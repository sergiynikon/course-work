import matplotlib.pyplot as plt
from numpy import *
from scitools.StringFunction import StringFunction
import numpy as np

def create_f(f):
    """
    creates function from string expression
    :param f: str
    :return: function
    """
    return StringFunction(f, independent_variables=('x'), globals=globals())

def plot_f(f, minvalue, maxvalue, n = 100):
    x = np.linspace(minvalue, maxvalue, n)
    y = f(x)
    plt.plot(x, y)
    plt.show()
