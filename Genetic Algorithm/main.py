from scitools.StringFunction import StringFunction

from Population import Population


def create_f(f):
    """
    creates function from string expression
    :param f: str
    :return: function
    """
    return StringFunction(f, independent_variables=('x'))


if __name__ == '__main__':
    pop_size = 100
    mutate_prob = 0.01
    retain = 0.1
    random_retain = 0.03
    a = -10
    b = 10
    f = create_f("x**4 - 3*x**3+x-1")
    pop = Population(f,
                     minvalue=a,
                     maxvalue=b,
                     pop_size=pop_size,
                     mutate_prob=mutate_prob,
                     retain=retain,
                     random_retain=random_retain)

    GENERATIONS = 100
    for x in range(GENERATIONS):
        pop.evolve()
        print(pop.fitness_history[-1])
    print("Generation:", x, "Population fitness:", pop.fitness_history[-1])

# TODO fix bugs where is infinite loop of calculating