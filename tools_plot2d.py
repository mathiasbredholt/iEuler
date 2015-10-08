import numpy as np
import matplotlib.pyplot as plt
import mathlib as ml


def plot(expr, func=None):
    t = np.arange(0.0, 2.0, 0.0001)
    s = np.sin(2 * np.pi * t)
    plt.plot(t, s)
    plt.xlabel(func.args[0].name)
    plt.ylabel('{}({})'.format(func.name, func.args[0].name))
    plt.grid(True)
    plt.savefig('plot.png')


plot(0)
