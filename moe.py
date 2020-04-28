import gym
import numpy as np
import torch
from torch.autograd import Variable
import argparse
import uuid
import random
import importlib

import math
import torch.nn as nn
from torch.nn.functional import relu, avg_pool2d, softmax, sigmoid
import sys


class MOE(nn.Module):
    """
    Gated mixture of experts layer with 3-level hierarchy
    args:
        inputs: integer - size of the input
        hidden: an integer - hidden size of the experts
        outputs: integer - size of the output
        experts: an integer - number of experts
        fc1: fully connected layer 1
        fc2: fully connected layer 2
        fc3: fully connected layer 3
        shared_module_list: network shared by all intra-option policies

    """
    def __init__(self, inputs,hidden,outputs,experts, fc1,fc2,fc3, shared_module_list):
        super(MOE, self).__init__()
        self.module_list = nn.ModuleList()
        self.experts = experts
        self.hidden = hidden
        self.outsize = outputs
        self.fc1 = fc1
        self.fc2 = fc2
        self.fc3 = fc3

        self.g1 = nn.Linear(inputs,experts)
        self.module_list += [self.g1]
        self.g2 = nn.Linear(hidden,experts)
        self.module_list += [self.g2]
        self.g3 = nn.Linear(hidden,experts)
        self.module_list += [self.g3]
        self.module_list += shared_module_list
        
    def forward(self, x):
        ### layer 1: x -> myh1
        gate1 = softmax(self.g1(x)).view(1,-1)[0]
        h1 = {}
        for i in range(self.experts):
            h1[i] = relu(self.fc1[i](x))
            if i == 0:
                myh1 = gate1[i].contiguous().repeat(1,self.hidden)*h1[i]
            else:
                myh1 += gate1[i].contiguous().repeat(1,self.hidden)*h1[i]

        ### layer 2: myh1 -> myh2
        gate2 = softmax(self.g2(myh1))[0]
        h2 = {}
        for i in range(self.experts):
            h2[i] = relu(self.fc2[i](myh1))
            if i == 0:
                myh2 = gate2[i].contiguous().repeat(1,self.hidden)*h2[i]
            else:
                myh2 += gate2[i].contiguous().repeat(1,self.hidden)*h2[i]

        ### layer 3: myh2 -> out 
        gate3 = softmax(self.g3(myh2))[0]
        h3 = {}
        for i in range(self.experts):
            h3[i] = self.fc3[i](myh2)
            if i == 0:
                out = gate3[i].contiguous().repeat(1,self.outsize)*h3[i]
            else:
                out += gate3[i].contiguous().repeat(1,self.outsize)*h3[i]
        
        return out[0]
        
            