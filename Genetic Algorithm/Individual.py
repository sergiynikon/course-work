from codecs import decode
import struct
import numpy as np


class Intividual(object):


    def __init__(self, f, minvalue, maxvalue, number=None, mutate_prob = 0.01):
        if number is None:
            self.f = f
            self.mutate_prob = mutate_prob
            self.number = np.random.uniform(minvalue, maxvalue)
            self.bin_number = self.__float_to_bin()
        else:
            self.number = number
            self.mutate()


    def __bin_to_float(self):
        """
        Convert binary string to a float.
        :param b: binary
        :return:
        """

        def int_to_bytes(n, length):  # Helper function
            """ Int/long to byte string.

                Python 3.2+ has a built-in int.to_bytes() method that could be used
                instead, but the following works in earlier versions including 2.x.
            """
            return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]
        bf = int_to_bytes(int(self.bin_number, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
        return struct.unpack('>d', bf)[0]

    def __float_to_bin(self):
        """
        Converts float number to a binary string,
        :return: str
        """
        [d] = struct.unpack(">Q", struct.pack(">d", self.number))
        return '{:064b}'.format(d)

    def fitness(self):
        return self.f(self.number)

    def mutate(self):
        def change_character(str, index, ch):
            return str[:index] + ch + str[(index + 1):]
        if self.mutate_prob > np.random.rand():
            mutate_index = np.random.randint(len(self.bin_number) - 1)
            self.bin_number = \
                change_character(self.bin_number, mutate_index, '1') if self.bin_number[mutate_index] == '0' else \
                change_character(self.bin_number, mutate_index, '0')