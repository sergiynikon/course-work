from function_manipulation import read_data_from_file
import numpy as np
x = [2.0781866350444034, -2.0002441708929837, 1.9999961853027288]
A, b = read_data_from_file('matrix')

print(np.dot(A, x))