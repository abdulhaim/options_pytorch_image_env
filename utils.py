import gym
import numpy as np
import torch
import torch.nn as nn

from gym.wrappers import AtariPreprocessing, TransformReward
from gym.wrappers import FrameStack as FrameStack_

# from fourrooms import Fourrooms
from common.minipacman import MiniPacman

class LazyFrames(object):
    def __init__(self, frames):
        self._frames = frames

    def __array__(self, dtype=None):
        out = np.concatenate(self._frames, axis=0)
        if dtype is not None:
            out = out.astype(dtype)
        return out

    def __len__(self):
        return len(self.__array__())

    def __getitem__(self, i):
        return self.__array__()[i]


class FrameStack(FrameStack_):
    def __init__(self, env, k):
        FrameStack_.__init__(self, env, k)

    def _get_ob(self):
        assert len(self.frames) == self.k
        return LazyFrames(list(self.frames))

def make_env(env_name):
    if env_name == 'pacman':
        mode = 'regular'
        env = MiniPacman(mode, 1000)
    elif env_name == 'procgen_maze':
        env = gym.make("procgen:procgen-maze-v0")
    return env 

def generate_features(env_name,in_channels):
    if env_name == 'procgen_maze':
        # domain: https://github.com/openai/procgen
        features = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=2, stride=2),
            nn.ReLU(),
            nn.Conv2d(16, 16, kernel_size=1, stride=2),
            nn.ReLU(),
            nn.modules.Flatten(),
            nn.Linear(256, 256),
            nn.ReLU()
        )
    elif env_name == "pacman":
        # domain: https://github.com/higgsfield/Imagination-Augmented-Agents/blob/master/common/deepmind.py
        features = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Conv2d(16, 16, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.modules.Flatten(),
            nn.Linear(768, 256),
            nn.ReLU()
        )
    return features

def to_tensor(obs):
    obs = np.asarray(obs)
    obs = torch.from_numpy(obs).float()
    return obs
