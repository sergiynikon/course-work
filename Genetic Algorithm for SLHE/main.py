import functions
from Population import Population
import numpy as np


if __name__ == '__main__':
    pop_size = 150
    mutate_prob = 0.2
    percentage_of_mutants = 0.5
    lb= -10
    ub = 10
    GENERATIONS = 100

    A, b = functions.read_data_from_file('matrix')
    vector_length = len(b)
    print(vector_length)

    pop = Population(A,
                     b,
                     lb=lb,
                     ub=ub,
                     vector_length=vector_length,
                     pop_size=pop_size,
                     mutate_probability=mutate_prob,
                     percentage_of_mutants=percentage_of_mutants)


    for generation in range(GENERATIONS + 1):
        pop.evolve(generation, GENERATIONS)
    print("minimum:", pop.best)
    pop.plot(GENERATIONS)
