# -*- coding: utf-8 -*-
import numpy as np

"""Main module."""


def sigmoid(z):
    """Compute sigmoid activation function"""
    return 1/(1+np.exp(-z))

