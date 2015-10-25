import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import mathlib as ml
import modules.numpy.parser as pn
import modules.latex.parser


def plot(expr, var='x', from_x=-4, to_x=4, precision=500, func=None):
    plt.figure(figsize=(6, 5))
    t = np.arange(from_x, to_x, (to_x - from_x) / precision)
    pn.set_plot_variables({var: t})
    # plt.rc('text', usetex=True)
    plt.plot(t, pn.parse(expr.value), linewidth=2)
    if func:
        plt.xlabel('${}$'.format(func.value[0].value), fontsize=16)
        plt.ylabel('${}({})$'.format(func.name, func.value[0].value),
                   fontsize=16)
        # plt.title(
        #     '$' + modules.latex.parser.convert_expr(func) + '=' + modules.latex.parser.convert_expr(expr.value) +
        #     '$',
        #     fontsize=18,
        #     y=1.04)
    else:
        plt.xlabel('$x$', fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        # plt.title('$y=' + modules.latex.parser.convert_expr(expr.value) +
        #           '$', fontsize=18, y=1.04)
    plt.savefig('mathnotes.png', transparent=True)
    plt.clf()