import struct
from codecs import decode

import numpy as np

class Individual(object):

    def __init__(self,
                 minvalue: float,
                 maxvalue: float,
                 number = None,
                 mutate_prob: float = 0.01):
        """

        :param number: float number from minvalue to maxvaleu
        :param mutate_prob: probability of mutation
        """
        self.mutate_prob = mutate_prob
        if number is None:
            self.number = np.random.uniform(minvalue, maxvalue)
            self.chromosome = self.__float_to_bin()
        else:
            if isinstance(number, float):
                self.number = number
                self.chromosome = self.__float_to_bin()
            elif isinstance(number, str):
                self.chromosome = number
                self.number = self.__bin_to_float()
            self.mutate()

    def __bin_to_float(self):
        """
        Convert binary string to a float.
        :return: float number
        """

        def int_to_bytes(n, length):  # Helper function
            return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]

        bf = int_to_bytes(int(self.chromosome, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
        return struct.unpack('>d', bf)[0]

    def __float_to_bin(self):
        """
        Converts float number to a binary string,
        :return: binary representation of float number as string
        """
        [d] = struct.unpack(">Q", struct.pack(">d", self.number))
        return '{:064b}'.format(d)

    def fitness(self, f):
        """
        calculates fitness for the chromosome
        :param f: function
        :return: fitness of number
        """
        try:
            return f(self.number)
        except OverflowError:
            return float("inf")

    def mutate(self):
        """
        mutate one chromosome gene
        """

        # TODO check if change_character change characters for len of str <= 2
        def change_character(str, index, ch):
            return str[:index] + ch + str[(index + 1):]

        if self.mutate_prob > np.random.rand():
            mutate_index = np.random.randint(len(self.chromosome) - 1)
            if self.chromosome[mutate_index] == '0':
                self.chromosome = change_character(self.chromosome, mutate_index, '1')
            else:
                self.chromosome = change_character(self.chromosome, mutate_index, '0')
