import numpy as np
import matplotlib.pyplot as plt

class Population:
    def __init__(self,
                 A:                     list,
                 b:                     list,
                 lb:                    float,
                 ub:                    float,
                 vector_length:         int,
                 pop_size:              int,
                 mutate_probability:    float,
                 percentage_of_mutants: float):

        self.A = A
        self.b = b
        self.lb = lb
        self.ub = ub
        self.vector_length = vector_length
        self.pop_size = pop_size
        self.mutate_probability = mutate_probability
        self.number_of_mutants = int(percentage_of_mutants * self.vector_length)
        self.quantity_random_individuals = int(0.2 * pop_size) # take 20% of individuals as random in tournament selection of parents
        print("quantity_random_individuals = ",self.quantity_random_individuals)
        self.fitness_history = []

        self.individuals = [None] * self.pop_size
        for i in range(self.pop_size):
            self.individuals[i] =  np.random.uniform(lb, ub, size=self.vector_length)
        self.best = self.individuals[0]

    def sort_individuals_and_select_best(self):
        """
        Sort individuals by fitness
        (we use reversed because in this case lower fintess is better)
        """
        self.individuals = list(reversed(sorted(self.individuals,
                                                key=lambda x: self.fitness(x),
                                                reverse=True)))

        # select best
        if self.fitness(self.individuals[0]) < self.fitness(self.best):
            self.best = self.individuals[0]

    def fitness(self, x):
        """

        :param A: matrix of numbers
        :param b: vector of right parts
        :return: fitness value for current individual x
        """
        return np.linalg.norm(np.dot(self.A, x) - self.b)

    def mutate(self, x, gen, max_gen):
        def universal_mutation(number):
            def r():
                b = 5
                s = np.random.rand() # number from 0 to 1
                return 1 - s**(1-gen/max_gen)**b

            lbm = max(self.lb, number - (self.ub - self.lb) * r())
            ubm = min(self.ub, number + (self.ub - self.lb) * r())
            return np.random.uniform(lbm, ubm)

        if self.mutate_probability > np.random.rand():
            mutant_indexes = np.random.randint(0, self.vector_length, self.number_of_mutants)
            for mutant_index in mutant_indexes:
                x[mutant_index] = universal_mutation(x[mutant_index])

        return x


    def select_parents(self):
        """
        in this method we use TOURNAMENT selection of parents:
        select random individuals and from these select the best individual as parent
        """
        # select random individuals:
        random_individuals_indexes = np.random.choice(self.pop_size,
                                                      size=self.quantity_random_individuals)
        random_individuals = []
        for i in range(self.quantity_random_individuals):
            random_individuals.append(self.individuals[random_individuals_indexes[i]])

        sorted_random_individuals = list(reversed(sorted(random_individuals,
                                                key=lambda x: self.fitness(x),
                                                reverse=True)))
        parent1 = sorted_random_individuals[0]
        parent2 = sorted_random_individuals[1]

        return parent1, parent2

    def grade(self, generation=None):
        """
        Grade the generation by getting the average fitness of its individuals
        """

        fitnesses = [self.fitness(x) for x in self.individuals]
        mean_fitness = np.mean(fitnesses)
        self.fitness_history.append(mean_fitness)

        if generation is not None:
            print("Generation ", generation, "\tPopulation fitness:", mean_fitness)

    def plot(self, num_generations):
        x = np.arange(num_generations + 1)
        y = self.fitness_history
        plt.plot(x, y)
        plt.show()

    def next_generation(self):
        """
        Crossover the parents gor generating children and new generation of individuals
        """

        def crossover(parent1, parent2):
            """
            crossover parents to generate child

            :param parent1: first parent
            :param parent2: second parent
            :return: child
            """

            child = [None] * self.vector_length
            for i in range(self.vector_length):
                child[i] = np.random.uniform(parent1[i], parent2[i])

            return child

        new_individuals = []
        for i in range(self.pop_size):
            new_individuals.append(crossover(*self.select_parents()))
        self.individuals = new_individuals

    def evolve(self, gen, max_gen):

        # mutate
        for i in range(self.pop_size):
            self.individuals[i] = self.mutate(self.individuals[i], gen, max_gen)

        self.next_generation()
        self.sort_individuals_and_select_best()

        self.grade(gen)

