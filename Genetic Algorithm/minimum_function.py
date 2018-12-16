import numpy as np
import GA
import matplotlib.pyplot as plt


class Genetics(object):

    def __init__(self, f, left, right, pop_weight=10, chromosome_length=8, num_generations=100):
        self.f = f  # function to find the minimum
        self.left = left  # left border of function
        self.right = right  # right border of function
        self.pop_size = (pop_weight, chromosome_length)
        self.population = self.init_population()  # first population
        self.fitness = GA.fitness(self.f, self.population)
        self.generation = 0
        self.num_generations = num_generations
        self.mutation_prob = 0.05
        self.fitness_history = [np.min(self.fitness)]
        self.minimum_function = np.min(self.fitness)

    def init_population(self):
        return np.random.uniform(self.left, self.right,
                                 size=(self.pop_size[0], self.pop_size[1]))

    def next_generation(self):
        self.fitness = GA.fitness(self.f, self.population)
        parents = GA.select_parents(self.population,
                                    self.fitness)
        min_fitness = np.min(self.fitness)
        if min_fitness < self.minimum_function:
            self.minimum_function = min_fitness
        self.fitness_history.append(min_fitness)
        plt.scatter(self.left, np.min(self.fitness), marker='o', c='red')
        offspring_crossover = GA.crossover(parents,
                                           offspring_size=((self.pop_size[0] -
                                                            parents.shape[0],
                                                            self.pop_size[1])))
        offspring_mutation = offspring_crossover
        if np.random.random() < self.mutation_prob:
            offspring_mutation = GA.mutation(offspring_crossover,
                                             self.left,
                                             self.right)

        # creating new population

        self.population[0:parents.shape[0], :] = parents
        self.population[parents.shape[0]:, :] = offspring_mutation

        self.generation += 1

    def show(self):
        print("generation: {0}".format(self.generation))
        print("population:\n{0}".format(self.population))
        print("minimum fitness: {0}".format(np.min(self.fitness)))

        # print("best solution: {0}".format(self.population[min_fitness_idx, :]))
        # print("best solition fitness: {0}".format(
        #     self.fitness[min_fitness_idx]))

    def plot(self):
        x = np.arange(self.left, self.right, 0.01)
        y = self.f(x)
        plt.plot(x, y)
        # plt.plot(self.f(np.min(self.fitness)), 'o')

    def histogram_fitness(self):
        plt.plot(np.arange(self.num_generations + 1), self.fitness_history)
        plt.plot(np.arange(self.num_generations + 1),
                 np.ones(self.num_generations + 1) * self.minimum_function, 'r-')
        plt.annotate('minimum function: {}'.format(self.minimum_function),
                     xy=(self.num_generations + 1, self.minimum_function), xytext=(self.num_generations / 3, self.minimum_function + 1),
                     arrowprops=dict(arrowstyle="->"))

    def loop(self):
        for i in range(self.num_generations):
            # self.show()

            self.next_generation()


def main():
    ga = Genetics(lambda x: np.exp(-x) * np.cos(2 * np.pi * x),
                  -4, 4)
    ga.loop()
    ga.plot()
    plt.show()
    ga.histogram_fitness()
    plt.show()


if __name__ == "__main__":
    main()
