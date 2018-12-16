import numpy as np


def fitness(f, population):
    return np.min(f(population), axis=1)


def select_parents(population, fitness, num_parents=2):
    # roulette wheel choice
    parents = np.empty((num_parents, population.shape[1]))
    # normalized_fitness = \
    #     fitness / np.linalg.norm(fitness)  # values from 0 to 1

    # my way to set up fitnesses with positive numbers
    normalized_fitness = \
        1 - (fitness - np.min(fitness)) / (np.max(fitness) - np.min(fitness))
    selection_probs = normalized_fitness / np.sum(normalized_fitness)

    for i in range(num_parents):
        parents_idx = np.random.choice(population.shape[0],
                                       p=selection_probs)
        # this implements for different parents
        normalized_fitness[i] = 0
        selection_probs = normalized_fitness / np.sum(normalized_fitness)

        parents[i, :] = population[parents_idx, :]

    return parents


def crossover(parents, offspring_size):
    # offspring = np.empty(offspring_size)
    # crossover_point = np.uint8(offspring_size[1] / 2)
    # for k in range(offspring_size[0]):
    #     offspring[k, 0:crossover_point] = \
    #         parents[0, 0:crossover_point]
    #     offspring[k, crossover_point:] = \
    #         parents[1, crossover_point:]

    # whole ariphmetic crossover
    alpha = 0.6
    offspring = np.empty(offspring_size)
    for k in range(offspring_size[0]):
        offspring[k, :] = alpha * parents[0] + (1 - alpha) * parents[1]
        return offspring


def mutation(offspring_crossover, left, right):
        # mutation change only 1 gene in each offspring randomly
    number_of_mutated_genes = 2
    gene_index = np.random.choice(offspring_crossover.shape[1],
                                  size=number_of_mutated_genes,
                                  replace=False)
    for i in range(offspring_crossover.shape[0]):
        random_values = np.random.uniform(left, right, number_of_mutated_genes)
        for j in range(number_of_mutated_genes):
            offspring_crossover[i, gene_index[j]] = random_values[j]
    return offspring_crossover
