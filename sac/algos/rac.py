from numbers import Number

import numpy as np
import tensorflow as tf

from rllab.core.serializable import Serializable
from utils import logger
from rllab.misc.overrides import overrides
from sac.policies import GaussianPolicy

from .base import RLAlgorithm

"""
CG: Renyi entropy regularized AC.
"""

EPS = 1e-6

class RAC(RLAlgorithm, Serializable):
    """
    See original SAC implementation for usage information.
    """

    def __init__(
            self,
            base_kwargs,

            env,
            policy,
            initial_exploration_policy,
            qf1,
            qf2,
            vf,
            pool,
            plotter=None,

            lr=3e-3,
            scale_reward=1,
            scale_entropy=1,
            discount=0.99,
            tau=0.01,
            target_update_interval=1,
            action_prior='uniform',
            reparameterize=False,

            save_full_state=False,
            renyiQ = 2.0
    ):
        """
        See original SAC implementation for argument usage information.
        """

        Serializable.quick_init(self, locals())
        super(RAC, self).__init__(**base_kwargs)

        self._env = env
        self._policy = policy
        self._initial_exploration_policy = initial_exploration_policy
        self._qf1 = qf1
        self._qf2 = qf2
        self._vf = vf
        self._pool = pool
        self._plotter = plotter

        self._policy_lr = lr
        self._qf_lr = lr
        self._vf_lr = lr
        self._scale_reward = scale_reward
        self._scale_entropy = scale_entropy
        self._discount = discount
        self._tau = tau
        self._target_update_interval = target_update_interval
        self._action_prior = action_prior

        # Reparameterize parameter must match between the algorithm and the
        # policy actions are sampled from.
        assert reparameterize == self._policy._reparameterize
        self._reparameterize = reparameterize

        self._save_full_state = save_full_state

        # CG: the entropic index for Tsallis entropy regularizer.
        self._renyiQ = renyiQ

        self._Da = self._env.action_space.flat_dim
        self._Do = self._env.observation_space.flat_dim

        self._training_ops = list()

        self._init_placeholders()
        self._init_actor_update()
        self._init_critic_update()
        self._init_target_ops()

        # CG: initialize the variable for calculating log of sigma for the Gaussian policy.
        self._init_mu_log_sigma()

        # Initialize all uninitialized variables. This prevents initializing
        # pre-trained policy and qf and vf variables.
        uninit_vars = []
        for var in tf.global_variables():
            try:
                self._sess.run(var)
            except tf.errors.FailedPreconditionError:
                uninit_vars.append(var)
        self._sess.run(tf.variables_initializer(uninit_vars))


    @overrides
    def train(self):
        """Initiate training of the SAC instance."""

        self._train(self._env, self._policy, self._initial_exploration_policy, self._pool)

    def _init_placeholders(self):
        """Create input placeholders for the SAC algorithm.

        Creates `tf.placeholder`s for:
            - observation
            - next observation
            - action
            - reward
            - terminals
        """
        self._iteration_pl = tf.placeholder(
            tf.float32, shape=None, name='iteration')

        # CG: the observation placeholder for critic training.
        self._observations_critic_ph = tf.placeholder(
            tf.float32,
            shape=(None, self._Do),
            name='observation',
        )

        # CG: the observation placeholder for actor training.
        self._observations_actor_ph = tf.placeholder(
            tf.float32,
            shape=(None, self._Do),
            name='observation',
        )

        self._next_observations_ph = tf.placeholder(
            tf.float32,
            shape=(None, self._Do),
            name='next_observation',
        )

        self._actions_ph = tf.placeholder(
            tf.float32,
            shape=(None, self._Da),
            name='actions',
        )

        self._rewards_ph = tf.placeholder(
            tf.float32,
            shape=(None, ),
            name='rewards',
        )

        self._terminals_ph = tf.placeholder(
            tf.float32,
            shape=(None, ),
            name='terminals',
        )

        # CG: the placeholder for log of integral of pi^q with respect to action for input observations.
        self._log_integral_pi_q_ph = tf.placeholder(
            tf.float32,
            shape=(None,),
            name='log_sigma',
        )

    @property
    def scale_reward(self):
        if callable(self._scale_reward):
            return self._scale_reward(self._iteration_pl)
        elif isinstance(self._scale_reward, Number):
            return self._scale_reward

        raise ValueError(
            'scale_reward must be either callable or scalar')

    @property
    def scale_entropy(self):
        if callable(self._scale_entropy):
            return self._scale_entropy(self._iteration_pl)
        elif isinstance(self._scale_entropy, Number):
            return self._scale_entropy

        raise ValueError(
            'scale_entropy must be either callable or scalar')

    def _init_critic_update(self):
        """Create minimization operation for critic Q-function.

        Creates a `tf.optimizer.minimize` operation for updating
        critic Q-function with gradient descent, and appends it to
        `self._training_ops` attribute.

        See Equation (10) in [1], for further information of the
        Q-function update rule.
        """

        self._qf1_t = self._qf1.get_output_for(self._observations_critic_ph, self._actions_ph, reuse=True)  # N
        self._qf2_t = self._qf2.get_output_for(self._observations_critic_ph, self._actions_ph, reuse=True)  # N

        with tf.variable_scope('target'):
            vf_next_target_t = self._vf.get_output_for(self._next_observations_ph)  # N
            self._vf_target_params = self._vf.get_params_internal()

        ys = tf.stop_gradient(
            self.scale_reward * self._rewards_ph +
            (1 - self._terminals_ph) * self._discount * vf_next_target_t
        )  # N

        self._td_loss1_t = 0.5 * tf.reduce_mean((ys - self._qf1_t)**2)
        self._td_loss2_t = 0.5 * tf.reduce_mean((ys - self._qf2_t)**2)

        qf1_train_op = tf.train.AdamOptimizer(self._qf_lr).minimize(
            loss=self._td_loss1_t,
            var_list=self._qf1.get_params_internal()
        )
        qf2_train_op = tf.train.AdamOptimizer(self._qf_lr).minimize(
            loss=self._td_loss2_t,
            var_list=self._qf2.get_params_internal()
        )

        self._training_ops.append(qf1_train_op)
        self._training_ops.append(qf2_train_op)

    def _init_actor_update(self):
        """Create minimization operations for policy and state value functions.

        Creates a `tf.optimizer.minimize` operations for updating
        policy and value functions with gradient descent, and appends them to
        `self._training_ops` attribute.

        In principle, there is no need for a separate state value function
        approximator, since it could be evaluated using the Q-function and
        policy. However, in practice, the separate function approximator
        stabilizes training.

        See Equations (8, 13) in [1], for further information
        of the value function and policy function update rules.
        """

        # CG: the current implementation of this function only supports Gaussian policy.
        if not isinstance(self._policy, GaussianPolicy):
            raise NotImplementedError

        actions, log_pi, raw_actions, log_pi_raw = self._policy.actions_for_rac(observations=self._observations_actor_ph, with_log_pis=True)

        self._vf_t = self._vf.get_output_for(self._observations_actor_ph, reuse=True)  # N
        self._vf_params = self._vf.get_params_internal()

        if self._action_prior == 'normal':
            D_s = actions.shape.as_list()[-1]
            policy_prior = tf.contrib.distributions.MultivariateNormalDiag(loc=tf.zeros(D_s), scale_diag=tf.ones(D_s))
            policy_prior_log_probs = policy_prior.log_prob(actions)
        elif self._action_prior == 'uniform':
            policy_prior_log_probs = 0.0

        log_target1 = self._qf1.get_output_for(self._observations_actor_ph, actions, reuse=True)  # N
        log_target2 = self._qf2.get_output_for(self._observations_actor_ph, actions, reuse=True)  # N
        min_log_target = tf.minimum(log_target1, log_target2)

        # CG: the loss function for policy training is re-defined to pave the way for GEAC.
        policy_loss = -tf.reduce_mean(log_pi *
                                      tf.stop_gradient(
                                          (self.scale_entropy * self._renyiQ / (1. - self._renyiQ)) / tf.exp(self._log_integral_pi_q_ph) * (tf.exp((self._renyiQ - 1.) * log_pi) - 1.)
                                          + (log_target1 - self._vf_t)
                                      )
                            )

        policy_regularization_losses = tf.get_collection(
            tf.GraphKeys.REGULARIZATION_LOSSES,
            scope=self._policy.name)
        policy_regularization_loss = tf.reduce_sum(policy_regularization_losses)

        # CG: must include policy_regularization_loss to stabilize learning. This is likely because NNs will be trained much more frequently through Q-learning
        # and therefore can easily diverge significantly if regularization loss is absent, making the learning behavior unpredictable.
        policy_loss = (policy_loss + policy_regularization_loss)

        # We update the vf towards the min of two Q-functions in order to
        # reduce overestimation bias from function approximation error.
        self._vf_loss_t = 0.5 * tf.reduce_mean((
            self._vf_t - tf.stop_gradient(
                min_log_target + self.scale_entropy / (1. - self._renyiQ) * self._log_integral_pi_q_ph
            )
        )**2)

        policy_train_op = tf.train.AdamOptimizer(self._policy_lr).minimize(
            loss=policy_loss,
            var_list=self._policy.get_params_internal()
        )

        vf_train_op = tf.train.AdamOptimizer(self._vf_lr).minimize(
            loss=self._vf_loss_t,
            var_list=self._vf_params
        )

        self._training_ops.append(policy_train_op)
        self._training_ops.append(vf_train_op)

    def _init_target_ops(self):
        """Create tensorflow operations for updating target value function."""

        source_params = self._vf_params
        target_params = self._vf_target_params

        self._target_ops = [
            tf.assign(target, (1 - self._tau) * target + self._tau * source)
            for target, source in zip(target_params, source_params)
        ]

    def _init_mu_log_sigma(self):
        """
        CG: this function initializes the variables for calculating the logarithm of sigma.
        For this function to work, the policy used must be the Gaussian policy.
        :return: 
        """
        if not isinstance(self._policy, GaussianPolicy):
            raise NotImplementedError

        self._pi_mu, self._pi_log_sigma = self._policy.distribution_for(observations=self._observations_actor_ph, with_log_pis=True)

    def _calc_mu_log_sigma(self, observations):
        """
        CG: this function calculates the logarithm of sigma with respect to input observations.
        For this function to work, the policy used must be the Gaussian policy.
        :param observations: 
        :return: 
        """
        if not isinstance(self._policy, GaussianPolicy):
            raise NotImplementedError

        feed_dict = {
            self._observations_actor_ph: observations,
        }
        return self._sess.run((self._pi_mu, self._pi_log_sigma), feed_dict)

    def _calc_log_integral_pi_q_bounded(self, observations):
        """
        CG: this function calculates the log of the integral of pi^q with respect to action for input observations.
        For this function to work, the policy used must be the Gaussian policy.
        NOTE: it is important to bound the integral from above by 1.0.
        :param observations: 
        :return: 
        """
        import math
        if not isinstance(self._policy, GaussianPolicy):
            raise NotImplementedError

        mu_array, log_sigma_array = self._calc_mu_log_sigma(observations)

        # Numerically approximate the integration of each action dimension.
        integral_results = np.ones(len(mu_array))
        percentiles = np.array([-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28])
        for i, mu in enumerate(mu_array):
            log_sigma = log_sigma_array[i]

            for j, m in enumerate(mu):
                sigma = math.exp(log_sigma[j])
                percent_lam = lambda x: m + x * sigma

                # Generate multiple random values from a normal distribution.
                total = 0.0
                # samples = np.random.normal(m, sigma, 10)
                samples = np.array(list(map(percent_lam, percentiles)))
                for sample in samples:
                    total = total + \
                        math.pow(self._normal_probablity_density_function(sample, m, sigma), self._renyiQ - 1.) * \
                        math.pow(self._tanh_derivative_inv(sample), self._renyiQ - 1.)
                total = total / len(samples)
                integral_results[i] = integral_results[i] * total

            if integral_results[i] > 1.0 - EPS or math.isnan(integral_results[i]) or math.isinf(integral_results[i]):
                integral_results[i] = 1.0 - EPS
            integral_results[i] = math.log(integral_results[i])

        return integral_results

    def _normal_probablity_density_function(self, x, mu, sigma):
        import math

        return math.exp(-(x-mu)*(x-mu)/2./sigma/sigma) / math.sqrt(2.0 * math.pi) / sigma

    def _tanh_derivative_inv(self, x):
        import math

        return ((math.exp(x) + math.exp(-x)) / 2.0) ** 2

    @overrides
    def _init_training(self, env, policy, pool):
        super(RAC, self)._init_training(env, policy, pool)
        self._sess.run(self._target_ops)

    @overrides
    def _do_training(self, iteration, batch):
        """Runs the operations for updating training and target ops."""

        feed_dict = self._get_feed_dict(iteration, batch)
        self._sess.run(self._training_ops, feed_dict)

        if iteration % self._target_update_interval == 0:
            # Run target ops here.
            self._sess.run(self._target_ops)

    def _duplicate_observations(self, observations, duplicationTimes):
        """
        CG: The function that duplicates every given observation by a duplicationTimes number of times.
        :param observations: 
        :param duplicationTimes: 
        :return: 
        """
        obvs = np.array([ob for ob in observations for _ in range(duplicationTimes)])
        return obvs

    def _get_feed_dict(self, iteration, batch):
        """Construct TensorFlow feed_dict from sample batch."""

        obv_actor = self._duplicate_observations(batch['observations'], 1)
        log_integral_pi_q = self._calc_log_integral_pi_q_bounded(obv_actor)

        feed_dict = {
            self._observations_critic_ph: batch['observations'],
            self._observations_actor_ph: obv_actor,
            self._actions_ph: batch['actions'],
            self._next_observations_ph: batch['next_observations'],
            self._rewards_ph: batch['rewards'],
            self._terminals_ph: batch['terminals'],
            self._log_integral_pi_q_ph: log_integral_pi_q
        }

        if iteration is not None:
            feed_dict[self._iteration_pl] = iteration

        return feed_dict

    @overrides
    def log_diagnostics(self, iteration, batch):
        """Record diagnostic information to the logger.

        Records mean and standard deviation of Q-function and state
        value function, and TD-loss (mean squared Bellman error)
        for the sample batch.

        Also calls the `draw` method of the plotter, if plotter defined.
        """

        feed_dict = self._get_feed_dict(iteration, batch)
        qf1, qf2, vf, td_loss1, td_loss2 = self._sess.run(
            (self._qf1_t, self._qf2_t, self._vf_t, self._td_loss1_t, self._td_loss2_t), feed_dict)

        logger.record_tabular('qf1-avg', np.mean(qf1))
        logger.record_tabular('qf1-std', np.std(qf1))
        logger.record_tabular('qf2-avg', np.mean(qf1))
        logger.record_tabular('qf2-std', np.std(qf1))
        logger.record_tabular('mean-qf-diff', np.mean(np.abs(qf1-qf2)))
        logger.record_tabular('vf-avg', np.mean(vf))
        logger.record_tabular('vf-std', np.std(vf))
        logger.record_tabular('mean-sq-bellman-error1', td_loss1)
        logger.record_tabular('mean-sq-bellman-error2', td_loss2)

        self._policy.log_diagnostics(iteration, batch)
        if self._plotter:
            self._plotter.draw()

    @overrides
    def get_snapshot(self, epoch):
        """Return loggable snapshot of the SAC algorithm.

        If `self._save_full_state == True`, returns snapshot of the complete
        SAC instance. If `self._save_full_state == False`, returns snapshot
        of policy, Q-function, state value function, and environment instances.
        """

        if self._save_full_state:
            snapshot = {
                'epoch': epoch,
                'algo': self
            }
        else:
            snapshot = {
                'epoch': epoch,
                'policy': self._policy,
                'qf1': self._qf1,
                'qf2': self._qf2,
                'vf': self._vf,
                'env': self._env,
            }

        return snapshot

    def __getstate__(self):
        """Get Serializable state of the RLALgorithm instance."""

        d = Serializable.__getstate__(self)
        d.update({
            'qf1-params': self._qf1.get_param_values(),
            'qf2-params': self._qf2.get_param_values(),
            'vf-params': self._vf.get_param_values(),
            'policy-params': self._policy.get_param_values(),
            'pool': self._pool.__getstate__(),
            'env': self._env.__getstate__(),
        })
        return d

    def __setstate__(self, d):
        """Set Serializable state fo the RLAlgorithm instance."""

        Serializable.__setstate__(self, d)
        self._qf1.set_param_values(d['qf1-params'])
        self._qf2.set_param_values(d['qf2-params'])
        self._vf.set_param_values(d['vf-params'])
        self._policy.set_param_values(d['policy-params'])
        self._pool.__setstate__(d['pool'])
        self._env.__setstate__(d['env'])
