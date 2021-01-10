import re
from collections import defaultdict

import gym

from core.env import Env
from .atari import AtariEnv
from .kz import KZEnv
from .classic_control import ClassicControlEnv

mapping = {
    'atari': AtariEnv,
    'classic_control': ClassicControlEnv
    'kz': KZEnv
}


def _get_gym_env_type(env_id):
    """Modified from https://github.com/openai/baselines/blob/master/baselines/run.py"""
    game_envs = defaultdict(set)

    for env in gym.envs.registry.all():
        env_type = env.entry_point.split(':')[0].split('.')[-1]
        game_envs[env_type].add(env.id)  # This is a set so add is idempotent

    if env_id in game_envs.keys():
        env_type = env_id
    else:
        env_type = None
        for g, e in game_envs.items():
            if env_id in e:
                env_type = g
                break
        if ':' in env_id:
            env_type = re.sub(r':.*', '', env_id)

    return env_type


def get_env(env_id: str, **kwargs) -> Env:
    if env_id == 'kz':
        return KZEnv(**kwargs)
    env_type = _get_gym_env_type(env_id)

    if env_type is None:
        # Non-gym environments
        env_type = env_id
        if env_type not in mapping:
            ValueError(f'Unknown environment: {env_type}')

        return mapping[env_type](**kwargs)
    else:
        if env_type not in mapping:
            ValueError(f'Unknown environment: {env_type}')

        return mapping[env_type](env_id, **kwargs)
