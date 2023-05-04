import random

# Optimise the EMA values
def optimise_ema(backtest_func, ema_range, population_size, generations):
    # Define the fitness function
    def fitness(individual):
        ema1, ema2, ema3 = individual

        final_portfolio_value = backtest_func('data/kraken_data.csv', ema1=ema1, ema2=ema2, ema3=ema3)

        return final_portfolio_value,

    # Create the initial population
    population = [[random.choice(ema_range[0]), random.choice(ema_range[1]), random.choice(ema_range[2])] for _ in range(population_size)]

    # Iterate through generations
    for _ in range(generations):
        fitnesses = [fitness(individual) for individual in population]

        # Sort population based on fitness
        sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)

        new_population = []

        # Select the top individuals
        top_individuals = [x[0] for x in sorted_population[:int(population_size * 0.1)]]
        new_population.extend(top_individuals)

        # Create the next generation
        for i in range(population_size - len(top_individuals)):
            # Select parents for crossover
            parent1, parent2 = random.choices(sorted_population[:int(population_size * 0.5)], k=2)

            # Perform crossover and mutation
            crossover_point1, crossover_point2 = random.sample(range(3), 2)
            if crossover_point1 > crossover_point2:
                crossover_point1, crossover_point2 = crossover_point2, crossover_point1
            child = parent1[0][:crossover_point1] + parent2[0][crossover_point1:crossover_point2] + parent1[0][crossover_point2:]

            for j in range(3):
                if random.random() < 0.1:
                    child[j] = random.choice(ema_range[j])

            new_population.append(child)

        population = new_population

    fitnesses = [fitness(individual) for individual in population]

    sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)

    return sorted_population[0][0], sorted_population[0][1][0]