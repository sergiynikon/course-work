import function_manipulation
from Population import Population

if __name__ == '__main__':
    pop_size = 100
    mutate_prob = 0.01
    retain = 0.1
    random_retain = 0.03
    a = -2
    b = 1
    f = function_manipulation.create_f("sin(10*pi*x) + x")
    function_manipulation.plot_f(f, a, b)
    pop = Population(f,
                     minvalue=a,
                     maxvalue=b,
                     pop_size=pop_size,
                     mutate_prob=mutate_prob,
                     retain=retain,
                     random_retain=random_retain)

    GENERATIONS = 50
    for generation in range(GENERATIONS + 1):
        pop.evolve(generation)
    print("Generation:", generation, "minimum:", pop.minimum_function)
    pop.plot(GENERATIONS)
