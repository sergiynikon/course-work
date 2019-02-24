from codecs import decode
import numpy as np
import struct

def __bin_to_float(b):
    """
    Convert binary string to a float.
    :param b: binary
    :return:
    """
    bf = __int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
    return struct.unpack('>d', bf)[0]

def __int_to_bytes(n, length):  # Helper function
    """ Int/long to byte string.

        Python 3.2+ has a built-in int.to_bytes() method that could be used
        instead, but the following works in earlier versions including 2.x.
    """
    return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]

def __float_to_bin(value):
    """
    Converts float number to a binary string,
    :param value: float
    :return: str
    """
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    return '{:064b}'.format(d)

def float_to_bin(arr):
    """
    Converts 2-dim. numpy.array with float numbers
    to 2-dim. numpy.array with string binary numbers
    :param arr: numpy.array
    :return: numpy.array
    """
    if (isinstance(arr, np.ndarray)):

        bin_arr = [[''] * arr.shape[1] for _ in range(arr.shape[0])]
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                bin_arr[i][j] = __float_to_bin(arr[i][j])
        return np.array(bin_arr)

def bin_to_float(arr):
    """
    Converts 2-dim. numpy.array with string binary numbers
    to 2-dim. numpy.array with float numbers
    :param arr: numpy.array
    :return: numpy.array
    """
    if (isinstance(arr, np.ndarray)):
        float_arr = [[0.0] * arr.shape[1] for _ in range(arr.shape[0])]
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                float_arr[i][j] = __bin_to_float(arr[i][j])
        return np.array(float_arr)
