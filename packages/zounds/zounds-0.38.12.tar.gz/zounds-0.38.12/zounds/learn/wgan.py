from trainer import Trainer
import numpy as np


class WassersteinGanTrainer(Trainer):
    """
    Args:
        network (nn.Module): the network to train
        latent_dimension (tuple): A tuple that defines the shape of the latent
            dimension (noise) that is the generator's input
        n_critic_iterations (int): The number of minibatches the critic sees
            for every minibatch the generator sees
        epochs: The total number of passes over the training set
        batch_size: The size of a minibatch
        preprocess_minibatch (function): function that takes the current
            epoch, and a minibatch, and mutates the minibatch
        kwargs_factory (callable): function that takes the current epoch and
            outputs args to pass to the generator and discriminator
        on_batch_complete (callable): callable invoked after each epoch,
            accepting epoch and network being trained as arguments
    """

    def __init__(
            self,
            network,
            latent_dimension,
            n_critic_iterations,
            epochs,
            batch_size,
            preprocess_minibatch=None,
            kwargs_factory=None,
            on_batch_complete=None,
            debug_gradient=False):

        super(WassersteinGanTrainer, self).__init__(epochs, batch_size)
        self.debug_gradient = debug_gradient
        self.on_batch_complete = on_batch_complete
        self.arg_maker = kwargs_factory
        self.preprocess = preprocess_minibatch
        self.n_critic_iterations = n_critic_iterations
        self.latent_dimension = latent_dimension
        self.network = network
        self.critic = network.discriminator
        self.generator = network.generator
        self.samples = None

    def _minibatch(self, data):
        indices = np.random.randint(0, len(data), self.batch_size)
        return data[indices, ...]

    def _gradient_penalty(self, real_samples, fake_samples, kwargs):
        """
        Compute the norm of the gradients for each sample in a batch, and
        penalize anything on either side of unit norm
        """
        import torch
        from torch.autograd import Variable, grad

        real_samples = real_samples.view(fake_samples.shape)

        # computing the norm of the gradients is very expensive, so I'm only
        # taking a subset of the minibatch here
        # subset_size = min(10, real_samples.shape[0])
        subset_size = real_samples.shape[0]

        real_samples = real_samples[:subset_size]
        fake_samples = fake_samples[:subset_size]

        alpha = torch.rand(subset_size).cuda()
        alpha = alpha.view((-1,) + ((1,) * (real_samples.dim() - 1)))

        interpolates = alpha * real_samples + ((1 - alpha) * fake_samples)
        interpolates = Variable(interpolates.cuda(), requires_grad=True)

        d_output = self.critic(interpolates, **kwargs)

        gradients = grad(
            outputs=d_output,
            inputs=interpolates,
            grad_outputs=torch.ones(d_output.size()).cuda(),
            create_graph=True,
            retain_graph=True,
            only_inputs=True)[0]
        return ((gradients.norm(2, dim=1) - 1) ** 2).mean() * 10

    def freeze_generator(self):
        for p in self.generator.parameters():
            p.requires_grad = False

    def unfreeze_generator(self):
        for p in self.generator.parameters():
            p.requires_grad = True

    def freeze_discriminator(self):
        for p in self.critic.parameters():
            p.requires_grad = False

    def unfreeze_discriminator(self):
        for p in self.critic.parameters():
            p.requires_grad = True

    def _debug_network_gradient(self, network):
        if not self.debug_gradient:
            return

        for n, p in network.named_parameters():
            g = p.grad
            if g is not None:
                print(n, g.min().data[0], g.max().data[0], g.mean().data[0])

    def zero_generator_gradients(self):
        self._debug_network_gradient(self.generator)
        self.generator.zero_grad()

    def zero_discriminator_gradients(self):
        self._debug_network_gradient(self.critic)
        self.critic.zero_grad()

    def train(self, data):

        import torch
        from torch.optim import Adam
        from torch.autograd import Variable

        data = data.astype(np.float32)

        zdim = self.latent_dimension

        noise_shape = (self.batch_size,) + self.latent_dimension
        noise = torch.FloatTensor(*noise_shape)
        fixed_noise = torch.FloatTensor(*noise_shape).normal_(0, 1)

        self.generator.cuda()
        self.critic.cuda()
        noise, fixed_noise = noise.cuda(), fixed_noise.cuda()

        trainable_generator_params = (
            p for p in self.generator.parameters() if p.requires_grad)
        trainable_critic_params = (
            p for p in self.critic.parameters() if p.requires_grad)

        generator_optim = Adam(
            trainable_generator_params, lr=0.0001, betas=(0, 0.9))
        critic_optim = Adam(
            trainable_critic_params, lr=0.0001, betas=(0, 0.9))

        for epoch in xrange(self.epochs):
            if self.arg_maker:
                kwargs = self.arg_maker(epoch)
            else:
                kwargs = dict()

            for i in xrange(0, len(data), self.batch_size):
                self.zero_generator_gradients()
                self.zero_discriminator_gradients()

                self.freeze_generator()
                self.unfreeze_discriminator()

                for c in xrange(self.n_critic_iterations):

                    self.zero_discriminator_gradients()

                    minibatch = self._minibatch(data)
                    inp = torch.from_numpy(minibatch)
                    inp = inp.cuda()
                    input_v = Variable(inp)

                    if self.preprocess:
                        input_v = self.preprocess(epoch, input_v)

                    d_real = self.critic.forward(input_v, **kwargs)

                    # train discriminator on fake data
                    noise.normal_(0, 1)
                    noise_v = Variable(noise, volatile=True)
                    fake = Variable(
                        self.generator.forward(noise_v, **kwargs).data)

                    if self.preprocess:
                        fake = self.preprocess(epoch, fake)

                    d_fake = self.critic.forward(fake, **kwargs)

                    real_mean = torch.mean(d_real)
                    fake_mean = torch.mean(d_fake)
                    gp = self._gradient_penalty(input_v.data, fake.data, kwargs)
                    d_loss = (fake_mean - real_mean) + gp
                    d_loss.backward()
                    critic_optim.step()


                self.zero_discriminator_gradients()
                self.zero_generator_gradients()

                self.unfreeze_generator()
                self.freeze_discriminator()

                # train generator
                noise.normal_(0, 1)
                noise_v = Variable(noise)
                fake = self.generator.forward(noise_v, **kwargs)

                if self.preprocess:
                    fake = self.preprocess(epoch, fake)

                self.samples = fake

                d_fake = self.critic.forward(fake, **kwargs)
                g_loss = -torch.mean(d_fake)
                g_loss.backward()
                generator_optim.step()

                gl = g_loss.data[0]
                dl = d_loss.data[0]
                rl = real_mean.data[0]

                if self.on_batch_complete:
                    self.on_batch_complete(epoch, self.network, self.samples)

                if i % 10 == 0:
                    print \
                        'Epoch {epoch}, batch {i}, generator {gl}, real {rl}, critic {dl}' \
                            .format(**locals())

        return self.network
