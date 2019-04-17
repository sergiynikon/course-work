import function_manipulation
from Population import Population
import numpy as np


if __name__ == '__main__':
    pop_size = 200
    mutate_prob = 0.01
    retain = 0.2
    random_retain = 0.08
    percentage_of_mutants = 0.4
    a = -10
    b = 10
    A, B = function_manipulation.read_data_from_file('matrix')
    vector_length = len(B)
    print(vector_length)

    pop = Population(A,
                     B,
                     minvalue=a,
                     maxvalue=b,
                     vector_length=vector_length,
                     pop_size=pop_size,
                     mutate_prob=mutate_prob,
                     retain=retain,
                     random_retain=random_retain,
                     percentage_of_mutants=percentage_of_mutants)

    GENERATIONS = 100
    for generation in range(GENERATIONS + 1):
        pop.evolve(generation)
    print("minimum:", pop.best.x)
    pop.plot(GENERATIONS)
