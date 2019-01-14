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
import tensorflow as tf

from sac.algos.eac import EAC


from utils import logger


def run_experiment(env, seed, scale_reward,
                   scale_entropy, num_of_train):
    tf.set_random_seed(seed)

    # environmentName = env
    environmentName = env

    print("Experiment: {}".format(environmentName))

    # Set up the sampler.
    sampler_params = {
        'max_path_length': 1000,
        'min_pool_size': 1000,
        'batch_size': 256,
    }

    # Set up the value function networks.
    M = 128
    N = 2

    base_kwargs = {
            'n_epochs': 1000,
            'epoch_length': 1000,
            'n_train_repeat': num_of_train,
            'n_initial_exploration_steps': 1000,
            'eval_render': False,
            'eval_n_episodes': 1,
            'eval_deterministic': True,
    }

    # Define a function for reward scaling.
    def incrementor(itr):
        return (0.5 + (0.8-0.5) * tf.minimum(itr/500000., 1.0))
    def decrementor(itr):
        return (0.8 - (0.8-0.6) * tf.minimum(itr/500000., 1.0))

    algorithm = EAC(
        environment_name=environmentName,
        algorithm_name='rac',
        lr=3.e-4,
        scale_reward=scale_reward,
        scale_entropy=scale_entropy,
        discount=0.99,
        tau=0.01,
        max_replay_buffer_size=1000000,
        sampler_params=sampler_params,
        value_func_layers_number=N,
        value_func_layer_size=M,
        policy_func_layers_number=N,
        policy_func_layer_size=M,
        base_ac_alg_params=base_kwargs,
        q_param_list=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        use_ucb=False,
        evaluation_strategy='ensemble'
    )

    algorithm.train()


def pybullet_arg_parser():
    """
    Added by Yiming (6/12/2018)
    Create an argparse.ArgumentParser for bullet environments
    """
    import argparse
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', help = 'environment ID', type = str,
                        default = "ThrowerBulletEnv-v0")
    parser.add_argument('--seed', help = 'RNG seed', type = int, default = 0)
    parser.add_argument('--scale-reward', type = float, default = 0.5)
    parser.add_argument('--scale-entropy', type = float, default = 0.6)
    parser.add_argument('--num-of-train', type = int, default = 1)
    return parser


def main():
    args = pybullet_arg_parser().parse_args()
    logger.configure(
        format_strs = ['stdout', 'log', 'csv'],
        log_suffix = "EAC-{}-Seed_{}-sr_{}-se_{}-nbt_{}-START-"
            .format(args.env,args.seed,args.scale_reward,args.scale_entropy, args.num_of_train))
    logger.log("Algorithm: EAC")
    logger.log("Environment: {}".format(args.env))
    logger.log("Seed: {}".format(args.seed))
    logger.log("scale-reward: {}".format(args.scale_reward))
    logger.log("numberOfTrain: {}".format(args.num_of_train))
    run_experiment(env = args.env, seed = args.seed, scale_reward = args.scale_reward,
                   scale_entropy = args.scale_entropy, num_of_train = args.num_of_train)


if __name__ == '__main__':
    main()
