"""
CG: the ensemble entropy-regularized AC algorithm.
"""

import gtimer as gt

from rllab.core.serializable import Serializable
from rllab.misc import logger
from sac.algos.rac import RAC
from sac.algos.sacv1 import SACV1
from sac.algos.tac import TAC
from sac.envs import GymEnv
from sac.misc import tf_utils
from sac.misc.sampler import SimpleSampler, rollouts
from sac.policies import GaussianPolicy
from sac.replay_buffers import SimpleReplayBuffer
from sac.value_functions import NNQFunction, NNVFunction
from sac.core.serializable import deep_clone

import tensorflow as tf

class EAC(Serializable):
    """
    CG: the class that implements the EAC algorithm.
    """

    def __init__(
            self,
            environment_name,
            algorithm_name,
            lr,
            scale_reward,
            scale_entropy,
            discount,
            tau,
            max_replay_buffer_size,
            sampler_params,
            value_func_layers_number,
            value_func_layer_size,
            policy_func_layers_number,
            policy_func_layer_size,
            base_ac_alg_params,
            q_param_list,
            use_ucb=False,
            evaluation_strategy='ensemble',
    ):
        """
        CG: the constructor.
        :param environment_name: the name of the environment in string. 
        :param algorithm_name: the name of the AC algorithm to be used in the ensemble.
        :param lr: the learning rate to be used in the ensemble.
        :param scale_reward: the reward scaling factor.
        :param scale_entropy: the entropy scaling factor.
        :param discount: the reward discount factor.
        :param tau: the target value function updating factor.
        :param max_replay_buffer_size: the maximum size of the replay buffer.
        :param sampler_params: extra parameter settings for the random sampler.
        :param value_func_layers_number: the number of hidden layers for the value network, i.e. V function and Q function.
        :param value_func_layer_size: the number of neurons of each hidden layer of the value network. 
        :param policy_func_layers_number: th number of hidden layers for the policy network.
        :param policy_func_layer_size: the number of neurons of each hidden layer of the policy network.
        :param base_ac_alg_params: base parameters for the AC algorithm.
        :param q_param_list: the list of q values for the ensemble. Each q value in the list represents one AC instance in the ensemble.
        :param use_ucb: an indicator regarding the use of ucb for selecting AC instances in the ensemble for exploration.
        :param evaluation_strategy: the strategy used for evaluation. We have two strategies available, 'ensemble' and 'best-policy'.
        """
        # Set up the environment.
        self._environment_name = environment_name
        self._env =  GymEnv(self._environment_name)

        # Set up the algorithm parameters.
        self._algorithm_name = algorithm_name
        self._lr = lr
        self._scale_reward = scale_reward
        self._scale_entropy = scale_entropy
        self._discount = discount
        self._tau = tau
        self._use_ucb = use_ucb
        self._evaluation_strategy = evaluation_strategy

        # Set up the replay buffer.
        self._max_replay_buffer_size = max_replay_buffer_size
        self._pool = SimpleReplayBuffer(env_spec=self._env.spec, max_replay_buffer_size=self._max_replay_buffer_size)

        # Set up the environment sampler.
        self._sampler_params = sampler_params
        self._sampler = SimpleSampler(**self._sampler_params)

        # Set up the required number of AC instances in the ensemble. Each AC instance has its own value network and policy network.
        self._alg_instances = []
        self._base_ac_params = base_ac_alg_params
        self._base_alg_params = dict(self._base_ac_params, sampler=self._sampler)
        for id, q_val in enumerate(q_param_list):
            # Set up the value function network for an AC instance.
            qf1 = NNQFunction(env_spec=self._env.spec, hidden_layer_sizes=tuple([value_func_layer_size for _ in range(value_func_layers_number)]), name=str(id) + 'qf1')
            qf2 = NNQFunction(env_spec=self._env.spec, hidden_layer_sizes=tuple([value_func_layer_size for _ in range(value_func_layers_number)]), name=str(id) + 'qf2')
            vf = NNVFunction(env_spec=self._env.spec, hidden_layer_sizes=tuple([value_func_layer_size for _ in range(value_func_layers_number)]), name=str(id) + 'vf')

            # Set up the policy network for an AC instance.
            policy = GaussianPolicy(
                env_spec=self._env.spec,
                hidden_layer_sizes=tuple([policy_func_layer_size for _ in range(policy_func_layers_number)]),
                squash=True,
                reparameterize=False,
                reg=1.e-3,
                name=str(id) + 'gaussian_policy'
            )
            initial_exploration_policy = policy

            # Set up an AC instance.
            if self._algorithm_name == 'sac':
                algorithm = SACV1(
                    base_kwargs=self._base_alg_params,
                    env=self._env,
                    policy=policy,
                    initial_exploration_policy=initial_exploration_policy,
                    pool=self._pool,
                    qf1=qf1,
                    qf2=qf2,
                    vf=vf,
                    lr=self._lr,
                    scale_reward=self._scale_reward,
                    scale_entropy=self._scale_entropy,
                    discount=self._discount,
                    tau=self._tau,
                    reparameterize=False,
                    target_update_interval=1,
                    action_prior='uniform',
                    save_full_state=False,
                )
            elif self._algorithm_name == 'tac':
                algorithm = TAC(
                    base_kwargs=self._base_alg_params,
                    env=self._env,
                    policy=policy,
                    initial_exploration_policy=initial_exploration_policy,
                    pool=self._pool,
                    qf1=qf1,
                    qf2=qf2,
                    vf=vf,
                    lr=self._lr,
                    scale_reward=self._scale_reward,
                    scale_entropy=self._scale_entropy,
                    discount=self._discount,
                    tau=self._tau,
                    reparameterize=False,
                    target_update_interval=1,
                    action_prior='uniform',
                    save_full_state=False,
                    tsallisQ=q_val,
                )
            elif self._algorithm_name == 'rac':
                algorithm = RAC(
                    base_kwargs=self._base_alg_params,
                    env=self._env,
                    policy=policy,
                    initial_exploration_policy=initial_exploration_policy,
                    pool=self._pool,
                    qf1=qf1,
                    qf2=qf2,
                    vf=vf,
                    lr=self._lr,
                    scale_reward=self._scale_reward,
                    scale_entropy=self._scale_entropy,
                    discount=self._discount,
                    tau=self._tau,
                    reparameterize=False,
                    target_update_interval=1,
                    action_prior='uniform',
                    save_full_state=False,
                    renyiQ=q_val,
                )
            else:
                raise NotImplementedError

            # Initialize the AC instance.
            algorithm._sess.run(tf.global_variables_initializer())

            # Put the initialized AC instance into the algorithm instance list.
            # Each element of the algorithm instance list is made up of
            #           the algorithm instance,
            #           the moving average performance of the instance,
            #           the number of times the instance has been used for exploration previously, and
            #           the UCB bound.
            self._alg_instances.append([algorithm, 0.0, 0.0, 0.0])

    def train(self):
        """
        CG: the function that conducts ensemble training.
        :return: 
        """
        # Set up parameters for the training process.
        self._n_epochs = self._base_ac_params['n_epochs']
        self._epoch_length = self._base_ac_params['epoch_length']
        self._n_train_repeat = self._base_ac_params['n_train_repeat']
        self._n_initial_exploration_steps = self._base_ac_params['n_initial_exploration_steps']
        self._eval_render = self._base_ac_params['eval_render']
        self._eval_n_episodes = self._base_ac_params['eval_n_episodes']
        self._eval_deterministic = self._base_ac_params['eval_deterministic']

        # Set up the evaluation environment.
        if self._eval_n_episodes > 0:
            with tf.variable_scope("low_level_policy", reuse=True):
                self._eval_env = deep_clone(self._env)

        # Set up the tensor flow session.
        self._sess = tf_utils.get_default_session()

        # Import required libraries for training.
        import random
        import math
        import operator
        import numpy as np

        # Initialize the sampler.
        alg_ins = random.choice(self._alg_instances)
        self._sampler.initialize(self._env, alg_ins[0].policy, self._pool)

        # Perform the training/evaluation process.
        num_episode = 0.
        with self._sess.as_default():
            gt.rename_root('RLAlgorithm')
            gt.reset()
            gt.set_def_unique(False)

            for epoch in gt.timed_for(range(self._n_epochs + 1), save_itrs=True):
                logger.push_prefix('Epoch #%d | ' % epoch)

                for t in range(self._epoch_length):
                    isEpisodeEnd = self._sampler.sample()

                    # If an episode is ended, we need to update performance statistics for each AC instance and
                    # pick randomly another AC instance for next episode of exploration.
                    if isEpisodeEnd:
                        num_episode = num_episode + 1.
                        alg_ins[1] = 0.9 * alg_ins[1] + 0.1 * self._sampler._last_path_return
                        alg_ins[2] = alg_ins[2] + 1.

                        if self._use_ucb:
                            # Select an algorithm instance based on UCB.
                            selected = False
                            for ains in self._alg_instances:
                                if ains[2] < 1.:
                                    alg_ins = ains
                                    selected = True
                                    break
                                else:
                                    ains[3] = ains[1] + math.sqrt(2.0 * math.log(num_episode) / ains[2])

                            if not selected:
                                alg_ins = max(self._alg_instances, key=operator.itemgetter(3))

                        else:
                            # Select an algorithm instance uniformly at random.
                            alg_ins = random.choice(self._alg_instances)
                            self._sampler.set_policy(alg_ins[0].policy)

                    if not self._sampler.batch_ready():
                        continue
                    gt.stamp('sample')

                    # Perform training over all AC instances.
                    for i in range(self._n_train_repeat):
                        batch = self._sampler.random_batch()
                        for ains in self._alg_instances:
                            ains[0]._do_training(iteration=t + epoch * self._epoch_length, batch=batch)
                    gt.stamp('train')

                # Perform evaluation after one full epoch of training is completed.
                if self._eval_n_episodes < 1:
                    continue

                if self._evaluation_strategy == 'ensemble':
                    # Use a whole ensemble of AC instances for evaluation.
                    paths = rollouts(self._eval_env, self, self._sampler._max_path_length, self._eval_n_episodes)

                elif self._evaluation_strategy == 'best-policy':
                    # Choose the AC instance with the highest observed performance so far for evaluation.
                    eval_alg_ins = max(self._alg_instances, key=operator.itemgetter(1))
                    with eval_alg_ins[0].policy.deterministic(self._eval_deterministic):
                        paths = rollouts(self._eval_env, eval_alg_ins[0].policy, self._sampler._max_path_length, self._eval_n_episodes)

                else:
                    paths = None

                if paths is not None:
                    total_returns = [path['rewards'].sum() for path in paths]
                    episode_lengths = [len(p['rewards']) for p in paths]
                    logger.record_tabular('return-average', np.mean(total_returns))
                    logger.record_tabular('return-min', np.min(total_returns))
                    logger.record_tabular('return-max', np.max(total_returns))
                    logger.record_tabular('return-std', np.std(total_returns))
                    logger.record_tabular('episode-length-avg', np.mean(episode_lengths))
                    logger.record_tabular('episode-length-min', np.min(episode_lengths))
                    logger.record_tabular('episode-length-max', np.max(episode_lengths))
                    logger.record_tabular('episode-length-std', np.std(episode_lengths))

                    self._eval_env.log_diagnostics(paths)
                    if self._eval_render:
                        self._eval_env.render(paths)

                # Produce log info after each episode of training and evaluation.
                times_itrs = gt.get_times().stamps.itrs
                eval_time = times_itrs['eval'][-1] if epoch > 1 else 0
                total_time = gt.get_times().total
                logger.record_tabular('time-train', times_itrs['train'][-1])
                logger.record_tabular('time-eval', eval_time)
                logger.record_tabular('time-sample', times_itrs['sample'][-1])
                logger.record_tabular('time-total', total_time)
                logger.record_tabular('epoch', epoch)

                self._sampler.log_diagnostics()

                logger.dump_tabular(with_prefix=False)
                logger.pop_prefix()

                gt.stamp('eval')

            # Terminate the sampler after the training process is completed.
            self._sampler.terminate()

    def reset(self, dones=None):
        """
        CG: the function required in order to support evaluation (or rollout) by using EAC as an ensemble of AC instances.
        :param dones: 
        :return: 
        """
        pass

    def get_action(self, observation):
        """
        CG: the function required in order to support evaluation (or rollout) by using EAC as an ensemble of AC instances.
        :param observation: 
        :return: 
        """
        import numpy as np

        # Collect all recommended actions.
        recommend_actions = []
        for ains in self._alg_instances:
            with ains[0].policy.deterministic(self._eval_deterministic):
                recommend_actions.append(ains[0].policy.get_action(observation))

        # Determine the value of performing each recommended action.
        action_values = np.zeros(len(recommend_actions))
        for i, ract in enumerate(recommend_actions):
            for ains in self._alg_instances:
                action_values[i] = action_values[i] + ains[0]._qf1.eval([observation], [ract[0]])[0]
            action_values[i] = action_values[i] / len(self._alg_instances)

        # Choose the recommended action with the highest value.
        act_ind = np.argmax(action_values)

        return recommend_actions[act_ind]
