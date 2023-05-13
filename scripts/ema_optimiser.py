import random
import numpy as np
import pandas as pd
import ta
import matplotlib.pyplot as plt

def calculate_portfolio(filename, window1, window2, window3):
    # Read the CSV file into a Pandas dataframe
    df = pd.read_csv(filename)
    
    # Calculate the exponential moving averages for different time periods
    df['ema'+str(window1)] = ta.trend.EMAIndicator(close=df['close'], window=window1).ema_indicator()
    df['ema'+str(window2)] = ta.trend.EMAIndicator(close=df['close'], window=window2).ema_indicator()
    df['ema'+str(window3)] = ta.trend.EMAIndicator(close=df['close'], window=window3).ema_indicator()

    # Add buy and sell flags based on EMA trends
    prev_flag = 'sell'
    for i in range(len(df)):
        buy_flag = (df['ema'+str(window1)][i] > df['ema'+str(window2)][i]) & (df['ema'+str(window1)][i] > df['ema'+str(window3)][i])
        sell_flag = (df['ema'+str(window1)][i] < df['ema'+str(window2)][i]) & (df['ema'+str(window1)][i] < df['ema'+str(window3)][i])

        if buy_flag and prev_flag == 'sell':
            df.at[i, 'flag'] = 'buy'
            prev_flag = 'buy'
        elif sell_flag and prev_flag == 'buy':
            df.at[i, 'flag'] = 'sell'
            prev_flag = 'sell'

    # Set up initial cash and stock holdings
    cash = 100.0
    stock = 0.0

    # Loop through each row in the dataframe and perform trades based on the buy and sell flags
    for i in range(len(df)):
        if df['flag'][i] == 'buy':
            # Buy stock at the close price and update cash and stock holdings
            value = df['close'][i]
            stock = (cash / value) * 0.98
            cash = 0.0

        elif df['flag'][i] == 'sell':
            # Sell all stock at the close price and update cash and stock holdings
            value = df['close'][i]
            cash = (stock * value) * 0.98
            stock = 0.0


    # If the last flag was not a sell flag, sell all remaining stock at the close price
    if stock > 0:
        cash = stock * df['close'][len(df)-1]
        stock = 0

    # Return the updated dataframe and final cash balance
    return cash

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
            #CroosOver Probability set to 1
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
        
        if ema1 >= ema2 or ema1 >= ema3:
            return -np.inf,
    
        if ema2 >= ema3 or ema2 <= ema1:
            return -np.inf,
        
        if ema3 <= ema2 or ema3 <= ema1:
            return -np.inf,
        
        #final_portfolio_value = backtest_func('data/kraken_train.csv', ema1=ema1, ema2=ema2, ema3=ema3)
        final_portfolio_value = calculate_portfolio('data/kraken_train.csv', ema1, ema2, ema3)

        return final_portfolio_value,

    # Create the initial population
    population = [[random.choice(ema_range[0]), random.choice(ema_range[1]), random.choice(ema_range[2])] for _ in range(population_size)]
    fitnesses = [fitness(individual) for individual in population]
    
    graph = pd.DataFrame(columns=['generation', 'best fitness'])

    # Iterate through generations
    for gen in range(generations):
        new_population = []
        mat_pool = []
        
        #Mating pool
        for i in range(population_size):
            winner = tournament_selection(population,fitnesses,3)
            mat_pool.append(winner)

        # Select pairs to realize croosover and post mutation
        num_pairs = int(population_size/2)
        for i in range(num_pairs):
            if len(mat_pool) < 2:
                break
            pair=random.sample(mat_pool,2)
            #ETA Parameter is set to 20 in CroosOver and Mutation Methods
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

        # Append new row to DataFrame with current generation and best fitness
        sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
        best_fitness = sorted_population[0][1][0]
        graph = pd.concat([graph, pd.DataFrame({'generation': [gen], 'best fitness': [best_fitness]})], ignore_index=True)

        #print("Top 3 Generation" + str(gen))
        #print(sorted_population[0])
        #print(sorted_population[1])
        #print(sorted_population[2])
        print(f'Completed generation: {gen}')

    # plot the two columns as a line graph
    print(graph.head())
    graph.plot(x='generation', y='best fitness', kind='line')
    plt.show()
    best_index = fitnesses.index(max(fitnesses))
    return population[best_index],fitnesses[best_index]
