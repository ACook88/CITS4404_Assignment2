import random

# Optimise the EMA values
def optimise_ema(backtest_func, ema_range, population_size, generations,low_bound,up_bound):
    #EA Algorithms for Tournament Selection, SBX CroosOver and  Polynomial Mutation
    def tournament_selection(population, fitness_values, tournament_size):
        tournament = random.sample(list(zip(population, fitness_values)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])[0]  # select the solution with the minimum fitness value
        return winner
    def sbx_crossover(p1, p2, eta, low_bound, up_bound):
        c1, c2 = p1[:], p2[:]
        for i in range(len(p1)):
            if random.random() < 1:
                if abs(p1[i] - p2[i]) > 1e-14:
                    if p1[i] < p2[i]:
                        c1[i], c2[i] = sbx_crossover_single(p1[i], p2[i], eta, low_bound[i], up_bound[i])
                    else:
                        c2[i], c1[i] = sbx_crossover_single(p2[i], p1[i], eta, low_bound[i], up_bound[i])
                else:
                    c1[i] = (p1[i] + p2[i]) / 2
                    c2[i] = (p1[i] + p2[i]) / 2
        return c1, c2

    def sbx_crossover_single(x1, x2, eta, low_bound, up_bound):
        u = random.random()
        if u <= 0.5:
            beta = (2*u)**(1/(eta+1))
        else:
            beta = (1/(2*(1-u)))**(1/(eta+1))
        c1 = 0.5*((x1+x2) - beta*(x2-x1))
        c2 = 0.5*((x1+x2) + beta*(x2-x1))
        c1 = min(max(c1, low_bound), up_bound)
        c2 = min(max(c2, low_bound), up_bound)
        return c1, c2
    
    def polynomial_mutation(solution, eta, low_bound, up_bound, mutation_prob):
        mutated_solution = solution[:]
        #print(mutated_solution)
        for i in range(len(solution)):
            if random.random() < mutation_prob:
                delta1 = (mutated_solution[i] - low_bound[i]) / (up_bound[i] - low_bound[i])
                delta2 = (up_bound[i] - mutated_solution[i]) / (up_bound[i] - low_bound[i])
                rand = random.random()
                if rand <= 0.5:
                    deltaq = (2*rand + (1 - 2*rand)*(1 - delta1)**(eta + 1))**(1/(eta + 1)) - 1
                else:
                    deltaq = 1 - (2*(1 - rand) + 2*(rand - 0.5)*(1 - delta2)**(eta + 1))**(1/(eta + 1))
                mutated_solution[i] += deltaq * (up_bound[i] - low_bound[i])
                mutated_solution[i] = min(max(mutated_solution[i], low_bound[i]), up_bound[i])
                mutated_solution[i] = int(mutated_solution[i])
            else:
                mutated_solution[i] = int(mutated_solution[i])
        return mutated_solution
    # Define the fitness function
    def fitness(individual):
        ema1, ema2, ema3 = individual

        final_portfolio_value = backtest_func('data/kraken_data.csv', ema1=ema1, ema2=ema2, ema3=ema3)

        return final_portfolio_value,

    # Create the initial population
    population = [[random.choice(ema_range[0]), random.choice(ema_range[1]), random.choice(ema_range[2])] for _ in range(population_size)]
    fitnesses = [fitness(individual) for individual in population]
    
    # Iterate through generations
    for gen in range(generations):
        new_population = []
        mat_pool = []
        
        #Mating pool
        for i in range(population_size):
            winner = tournament_selection(population,fitnesses,3)
            mat_pool.append(winner)

        # REMOVE - Select the top individuals
        # top_individuals = [x[0] for x in sorted_population[:int(population_size * 0.1)]]
        # new_population.extend(top_individuals)

        # Select pairs to realize croosover and post mutation
        num_pairs = int(population_size/2)
        for i in range(num_pairs):
            if len(mat_pool) < 2:
                break
            pair=random.sample(mat_pool,2)
            child1,child2 = sbx_crossover(pair[0],pair[1],20,low_bound,up_bound)
            child1 = polynomial_mutation(child1,20,low_bound,up_bound,0.3)
            child2 = polynomial_mutation(child2,20,low_bound,up_bound,0.3)
            mat_pool.remove(pair[0])
            mat_pool.remove(pair[1])
            new_population.append(child1)
            new_population.append(child2)

        new_fitness = [fitness(individual) for individual in new_population]
        
        #copy new solutions
        for i in range(population_size):
            population[i] = new_population[i]
            fitnesses[i] = new_fitness[i]
        #print the new population
        sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
        print("Top 3 Generation" + str(gen))
        print(sorted_population[0])
        print(sorted_population[1])
        print(sorted_population[2])

    best_index = fitnesses.index(max(fitnesses))
    return population[best_index],fitnesses[best_index]
