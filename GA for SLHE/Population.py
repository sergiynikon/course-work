import random

import matplotlib.pyplot as plt
import numpy as np
import sys
from Individual import Individual


class Population(object):

    def __init__(self,
                 A,
                 b,
                 minvalue:      float   = sys.float_info.min,
                 maxvalue:      float   = sys.float_info.max,
                 vector_length: int     = None,
                 pop_size:      int   = 100,
                 mutate_prob:   float   = 0.01,
                 retain:        float   = 0.2,
                 random_retain: float   = 0.03,
                 percentage_of_mutants  = 0.01):
        self.A = A
        self.b = b
        self.minvalue = minvalue
        self.maxvalue = maxvalue

        if vector_length is not None:
            self.vector_length = vector_length
        else:
            self.vector_length = 1

        self.pop_size = pop_size
        self.mutate_prob = mutate_prob
        self.retain = retain
        self.random_retain = random_retain
        self.percentage_of_mutants = percentage_of_mutants
        self.fitness_history = []
        self.parents = []

        #create individuals
        self.individuals = []
        for x in range(pop_size):
            self.individuals.append(Individual(np.random.uniform(minvalue, maxvalue, size=self.vector_length), percentage_of_mutants=self.percentage_of_mutants, mutate_prob=self.mutate_prob))
        self.best = self.individuals[0]

    def sort_individuals_and_select_best(self):
        """
        Sort individuals by fitness
        (we use reversed because in this case lower fintess is better)
        """
        self.individuals = list(reversed(sorted(self.individuals,
                                                key=lambda x: x.fitness(self.A, self.b),
                                                reverse=True)))

        # select best
        if self.individuals[0].fitness(self.A, self.b) < self.best.fitness(self.A, self.b):
            self.best = self.individuals[0]

    # def select_best(self):
    #     if self.individuals[0].fitness(self.A, self.b) < self.best.fitness(self.A, self.b):
    #         self.best = self.individuals[0]

    def select_parents(self):
        """
        select the fittest individuals to be the parents of next generation
        (lower fitness it better in this case)
        Also select a some random non-fittest individuals
        to help get us out of local minimums
        """

        # Keep the fittest as parents for next generation
        retain_length = int(self.retain * len(self.individuals))
        self.parents = self.individuals[:retain_length]

        # Randomly select some from unfittest and add to parents array
        unfittest = self.individuals[retain_length:]
        for unfit in unfittest:
            if self.random_retain > np.random.rand():
                self.parents.append(unfit)

    def grade(self, generation=None):
        """
        Grade the generation by getting the average fitness of its individuals
        """

        fitnesses = [individual.fitness(self.A, self.b) for individual in self.individuals]
        mean_fitness = np.mean(fitnesses)
        self.fitness_history.append(mean_fitness)

        if generation is not None:
            print("Episode", generation, "Population fitness:", mean_fitness)

    def plot(self, num_generations):
        x = np.arange(num_generations + 1)
        y = self.fitness_history
        plt.plot(x, y)
        plt.show()

    def next_generation(self):
        """
        Crossover the parents to generate children and new generation of individuals
        """
        def crossover(parent1: Individual, parent2: Individual):
            """
            crossover parents to generate child

            :param parent1: first parent
            :param parent2: second parent
            :return: child
            """
            child_chromosome = [None] * self.vector_length
            for i in range(self.vector_length):
                crossover_index = np.random.randint(len(parent1.chromosome[0]) - 1)
                child1_chromosome = parent1.chromosome[i][:crossover_index] + parent2.chromosome[i][crossover_index:]
                child2_chromosome = parent2.chromosome[i][:crossover_index] + parent1.chromosome[i][crossover_index:]
                child_chromosome[i] = random.choice([child1_chromosome, child2_chromosome])
            # child_chromosome = [parent1.x[i] + parent2.x[i] / 2 for i in range(self.vector_length)]
            return Individual(child_chromosome)

        target_children_size = self.pop_size - len(self.parents)
        children = []
        if len(self.parents) > 0:
            while len(children) < target_children_size:
                parent1 = (random.choice(self.parents))
                parent2 = (random.choice(self.parents))
                if parent1 != parent2:
                    child = crossover(parent1, parent2)
                    children.append(child)
            self.individuals = self.parents + children

    def evolve(self, generation=None):
        self.sort_individuals_and_select_best()
        # self.select_best()
        self.select_parents()
        self.next_generation()
        self.grade(generation)
        self.parents = []
