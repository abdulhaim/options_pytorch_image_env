import gym
import numpy as np
import torch

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
    mode = 'regular'
    return MiniPacman(mode, 1000)

def to_tensor(obs):
    obs = np.asarray(obs)
    obs = torch.from_numpy(obs).float()
    return obs
