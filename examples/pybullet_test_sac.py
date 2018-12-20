import inspect
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.abspath(os.path.join(os.getcwd(), os.pardir)), os.pardir)))
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0, parentdir)

from sac.algos.sacv1 import SACV1
from sac.envs.gym_env import GymEnv
from sac.policies import GaussianPolicy
from sac.replay_buffers.simple_replay_buffer import SimpleReplayBuffer
from sac.misc.sampler import SimpleSampler
from sac.value_functions import NNQFunction
from sac.value_functions import NNVFunction
import tensorflow as tf
from utils import logger


def run_experiment(env, seed, scale_reward,
                   scale_entropy, num_of_train):
    tf.set_random_seed(seed)

    # environmentName = "InvertedPendulumBulletEnv-v0"
    environmentName = env

    print("Experiment: {}".format(environmentName))

    # Set up the PyBullet environment.
    # env = normalize(gym.make(environmentName))
    env = GymEnv(environmentName)

    # Set up the replay buffer.
    pool = SimpleReplayBuffer(env_spec = env.spec, max_replay_buffer_size = 1000000)

    # Set up the sampler.
    sampler_params = {
        'max_path_length': 1000,
        'min_pool_size': 1000,
        'batch_size': 256,
    }
    sampler = SimpleSampler(**sampler_params)

    # Set up the value function networks.
    M = 128
    qf1 = NNQFunction(env_spec = env.spec, hidden_layer_sizes = (M, M), name = 'qf1')
    qf2 = NNQFunction(env_spec = env.spec, hidden_layer_sizes = (M, M), name = 'qf2')
    vf = NNVFunction(env_spec = env.spec, hidden_layer_sizes = (M, M))

    # Set up the policy network.
    # initial_exploration_policy = UniformPolicy(env_spec=env.spec)

    policy = GaussianPolicy(
        env_spec = env.spec,
        hidden_layer_sizes = (M, M),
        reparameterize = False,
        reg = 1e-3,
    )
    # policy = GMMPolicy(
    #     env_spec=env.spec,
    #     K=1,
    #     hidden_layer_sizes=(M, M),
    #     reparameterize=False,
    #     qf=qf1,
    #     reg=1.0e-3,
    # )

    initial_exploration_policy = policy

    base_kwargs = {
        'epoch_length': 1000,
        'n_train_repeat': num_of_train,
        'n_initial_exploration_steps': 1000,
        'eval_render': False,
        'eval_n_episodes': 1,
        'eval_deterministic': True,
    }
    base_kwargs = dict(base_kwargs, sampler = sampler)

    # Define a function for reward scaling.
    def incrementor(itr):
        return (0.5 + (0.8 - 0.5) * tf.minimum(itr / 500000., 1.0))

    def decrementor(itr):
        return (0.8 - (0.8 - 0.6) * tf.minimum(itr / 500000., 1.0))

    algorithm = SACV1(
        base_kwargs = base_kwargs,
        env = env,
        policy = policy,
        initial_exploration_policy = initial_exploration_policy,
        pool = pool,
        qf1 = qf1,
        qf2 = qf2,
        vf = vf,
        lr = 3.0e-4,
        scale_reward =scale_reward,  # CG: default 1.0, 0.5 for the lunarlander problem, 3.0 for the pendulum problem.
        scale_entropy = scale_entropy,  # CG: default 1.0.
        discount = 0.99,
        tau = 0.01,
        reparameterize = False,
        target_update_interval = 1,
        action_prior = 'uniform',
        save_full_state = False,
    )

    algorithm._sess.run(tf.global_variables_initializer())
    algorithm.train()


def pybullet_arg_parser():
    """
    Added by Yiming (6/12/2018)
    Create an argparse.ArgumentParser for bullet environments
    """
    import argparse
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', help = 'environment ID', type = str,
                        default = "InvertedPendulumSwingupBulletEnv-v0")
    parser.add_argument('--seed', help = 'RNG seed', type = int, default = 0)
    parser.add_argument('--scale-reward', type = float, default = 0.5)
    parser.add_argument('--scale-entropy', type = float, default = 1.0)
    parser.add_argument('--num-of-train', type = int, default = 1)
    return parser


def main():
    args = pybullet_arg_parser().parse_args()
    logger.configure(
        format_strs = ['stdout', 'log', 'csv'], log_suffix = "SAC-{}-Seed_{}-sr_{}-se_{}-nbt_{}-START-"
            .format(args.env,args.seed,args.scale_reward,args.scale_entropy,args.num_of_train))
    logger.log("Algorithm: SAC")
    logger.log("Environment: {}".format(args.env))
    logger.log("Seed: {}".format(args.seed))
    logger.log("scale-reward: {}".format(args.scale_reward))
    logger.log("scale_entropy: {}".format(args.scale_entropy))
    logger.log("numberOfTrain: {}".format(args.num_of_train))
    run_experiment(env = args.env, seed = args.seed, scale_reward = args.scale_reward,
                   scale_entropy = args.scale_entropy, num_of_train = args.num_of_train)


if __name__ == '__main__':
    main()
