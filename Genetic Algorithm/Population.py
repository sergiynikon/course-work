import random

import numpy as np

from Individual import Individual


class Population(object):

    def __init__(self,
                 f,
                 minvalue:      float,
                 maxvalue:      float,
                 pop_size:      float = 100,
                 mutate_prob:   float = 0.01,
                 retain:        float = 0.2,
                 random_retain: float = 0.03):
        self.f = f
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.pop_size = pop_size
        self.mutate_prob = mutate_prob
        self.retain = retain
        self.random_retain = random_retain
        self.fitness_history = []
        self.parents = []

        #create individuals
        self.individuals = []
        for x in range(pop_size):
            self.individuals.append(Individual(self.minvalue,
                                               self.maxvalue))

    def select_parents(self):
        """
        select the fittest individuals to be the parents of next generation
        (lower fitness it better in this case)
        Also select a some random non-fittest individuals
        to help get us out of local minimums
        """
        # Sort individuals by fitness
        # (we use reversed because in this case lower fintess is better)
        self.individuals = list(reversed(sorted(self.individuals, key=lambda x: x.fitness(self.f), reverse=True)))
        self.fitness_history.append(self.individuals[0].fitness(self.f))
        # Keep the fittest as parents for next generation
        retain_length = int(self.retain * len(self.individuals))
        self.parents = self.individuals[:retain_length]

        # Randomly select some from unfittest and add to parents array
        unfittest = self.individuals[retain_length:]
        for unfit in unfittest:
            if self.random_retain > np.random.rand():
                self.parents.append(unfit)

    # def grade(self, generation=None):
    #     """
    #     Grade the generation by getting the average fitness of its individuals
    #     """
    #     fitness_sum = 0
    #     for x in self.individuals:
    #         fitness_sum += x.fitness(self.f)
    #
    #     pop_fitness = fitness_sum / self.pop_size
    #     self.fitness_history.append(pop_fitness)
    #
    #     if generation is not None:
    #         if generation % 5 == 0:
    #             print("Episode", generation, "Population fitness:", pop_fitness)

    def next_generation(self):
        """
        Crossover the parents to generate children and new generation of individuals
        """
        def crossover(parent1: str, parent2: str):
            """
            crossover parents to generate child

            :param parent1: first parent
            :param parent2: second parent
            :return: child
            """
            crossover_index = np.random.randint(len(parent1) - 1)
            child1 = parent1[:crossover_index] + parent2[crossover_index:]
            child2 = parent2[:crossover_index] + parent1[crossover_index:]
            child = random.choice([child1, child2])
            return Individual(self.minvalue, self.maxvalue, child)

        target_children_size = self.pop_size - len(self.parents)
        children = []
        if len(self.parents) > 0:
            while len(children) < target_children_size:
                parent1 = (random.choice(self.parents)).chromosome
                parent2 = (random.choice(self.parents)).chromosome
                if parent1 != parent2:
                    child = crossover(parent1, parent2)
                    children.append(child)
            self.individuals = self.parents + children

    def evolve(self):
        self.select_parents()
        self.next_generation()

        self.parents = []
