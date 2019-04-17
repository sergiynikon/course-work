import random
import struct
from codecs import decode
import sys
import numpy as np

class Individual(object):

    def __init__(self,
                 vector                         = None,
                 percentage_of_mutants: float   = 0.5,
                 mutate_prob:           float   = 0.01):

        """
        :param x: vector from minvalue to maxvaleu
        :param mutate_prob: probability of mutation
        """
        self.vector_length = len(vector)
        if isinstance(vector[0], float):
            self.x = vector
            self.chromosome = self.__float_to_bin()
        elif isinstance(vector[0], str):
            self.chromosome = vector
            self.x = self.__bin_to_float()
        self.mutate_prob = mutate_prob
        self.number_of_mutants = int(percentage_of_mutants * self.vector_length)
        self.chromosome = self.__float_to_bin()
        self.mutate()

    def __bin_to_float(self):
        """
        Convert binary array to a float array
        :return: float array x
        """

        def int_to_bytes(n, length):  # Helper function
            return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]

        result = []
        for i in range(self.vector_length):
            bf = int_to_bytes(int(self.chromosome[i], 2), 8)  # 8 bytes needed for IEEE 754 binary64.
            result.append(struct.unpack('>d', bf)[0])
        return result

    def __float_to_bin(self):
        """
        Converts float vector x to a binary vector of strings,
        :return: binary representation of float x as string
        """
        result = []
        for i in range(self.vector_length):
            [d] = struct.unpack(">Q", struct.pack(">d", self.x[i]))
            result.append('{:064b}'.format(d))
        return result

    def fitness(self, A, b):
        """
        calculates fitness for the chromosome
        :param A: Matrix
        :param b: array
        :return: fitness of x
        """
        try:
            return np.linalg.norm(np.dot(A, self.x) - b)
        except OverflowError:
            return sys.float_info.max

    def mutate(self):
        """
        mutate chromosome genes (percentage_of_mutants - percentage of mutant genes)
        """
        def change_allele(str, index, ch):
            return str[:index] + ch + str[(index + 1):]

        if self.mutate_prob > np.random.rand():
            mutant_indexes = np.random.randint(0, self.vector_length, self.number_of_mutants)
            for mutant_index in mutant_indexes:
                mutant_allele_index = np.random.randint(50, 64) # 64 because every chromosome consist of 64-bit number
                if self.chromosome[mutant_index][mutant_allele_index] == '0':
                    self.chromosome[mutant_index] = \
                        change_allele(self.chromosome[mutant_index], mutant_allele_index, '1')
                else:
                    self.chromosome[mutant_index] = \
                        change_allele(self.chromosome[mutant_index], mutant_allele_index, '0')

        self.x = self.__bin_to_float()

