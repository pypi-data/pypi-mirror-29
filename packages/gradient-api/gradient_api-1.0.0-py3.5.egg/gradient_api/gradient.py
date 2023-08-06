# coding=utf-8
# uliontse

import numpy as np
from sympy import Symbol,diff
import matplotlib.pyplot as plt


def generate(expr_or_poly1d,init_x=-10.0,step=0.1,num_iters=None,showPlot=True):
    cur_x = np.array([init_x])[0]
    step = np.array([step])[0]
    num_iters = num_iters or 10000

    if isinstance(expr_or_poly1d,str):
        expr = expr_or_poly1d
        x = Symbol('x')
        diff_expr = str(diff(eval(expr),x))
        gradient = lambda x: np.array([eval(diff_expr)])[0]
        y = lambda x: np.array([eval(expr)])[0]

    elif isinstance(expr_or_poly1d,list) or isinstance(expr_or_poly1d,np.ndarray) or isinstance(expr_or_poly1d,tuple):
        L = expr_or_poly1d
        y = np.poly1d(L)
        gradient = np.poly1d.deriv(y)

    else:
        print("TypeError: Param 'expr_or_poly1d' is not 'str' or 'array1d_like'")
        return

    plot_x = np.linspace(init_x-5,init_x+15,201)
    plot_y = y(plot_x)
    plt.ion()

    cur_num = 0
    for i in range(num_iters):
        cur_num += 1
        prev_x = cur_x
        cur_x -= step * gradient(prev_x)
        if abs(y(cur_x) - y(prev_x)) < np.array([1e-8])[0]:
            break
        if showPlot and i % 2 == 0:
            # plt.cla()
            plt.plot(plot_x, plot_y)
            plt.scatter(cur_x, y(cur_x), color='red')
            plt.pause(0.1)
    plt.ioff()
    plt.show()
    return {
        'X': cur_x,
        'Y': y(cur_x),
        'Gradient': gradient(cur_x),
        'Numloop': cur_num
    }
