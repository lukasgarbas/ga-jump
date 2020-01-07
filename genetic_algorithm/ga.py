from simulation import Simulation
from figure import Figure
from typing import List
import random
import copy

class Individual:
    '''Individual is represented by
        
    its actions (list of integers between 0 and 4) and a score.
    score will be set after running the simulation and evaluating
    individual actions   
    '''
    def __init__(self, actions: List[int]):
        self.actions = actions
        self.score = 0.0

    def set_score(self, score: float) -> None:
        self.score = score


class GeneticAlgorithm:
    def __init__(
        self, figure: Figure, population_size: int, num_generations: int, 
        simulation_runtime: float = 7.5, crossover_rate:float = 0.5, 
        elitism_size: float = 0.1, crossover_size=0.4
        ):
        self.figure = figure
        self.sim_runtime = simulation_runtime
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_rate = crossover_rate
        self.elitism_size = elitism_size
        self.crossover_size = crossover_size
        self.individual_size = self.calculate_timesteps()
        self.best_individual = None

    def calculate_timesteps(self) -> int:
        return int(self.sim_runtime / 0.25)

    def random_population(self, population_size: int) -> List[Individual]:
        '''Creates a random population
        
        Generates lists of actions with random numbers from 0 to 4
        creates a population out of random individuals 
        '''
        population = []
        for x in range(population_size):
            actions = [random.randint(0, 4) for _ in range(self.individual_size)]
            individual = Individual(actions)
            population.append(individual)
        return population

    def evaluate_population(self, population) -> None:
        population.sort(key = lambda population: population.score)

    def create_next_population(self, population_sorted) -> List[Individual]:
        '''Creates a new population 
        
        New population consists of elites, crossovers, and random individuals
        '''
        new_population = []
        num_elites = int(self.population_size * self.elitism_size)
        num_crossovers = int(self.population_size * self.crossover_size)
        num_random = self.population_size - num_elites - num_crossovers
        for n in range(num_elites):
            new_population.append(population_sorted[n])
        for n in range(num_crossovers):
            rd_elite = population_sorted[random.randint(0, num_elites - 1)].actions
            rd_non_elite = population_sorted[random.randint(num_elites, self.population_size -1)].actions
            mutant = self.crossover(rd_elite, rd_non_elite)
            new_population.append(mutant)
        random_individuals = self.random_population(num_random)
        new_population = new_population + random_individuals
        return new_population

    def crossover(self, elite, non_elite) -> Individual:
        '''Performs uniform crossover'''
        mutation = []
        for i in range(len(elite)):
            rd = random.uniform(0, 1)
            if rd > self.crossover_rate:
                mutation.append(non_elite[i])
            else:
                mutation.append(elite[i])
        new_individual = Individual(mutation)
        return new_individual

    def run(self) -> None:
        '''Runs for n generations 
        
        Creates a simulation with the default figure and the action list 
        provided in the individual. Evaluates (sorts) the population by 
        individual score and generates the next population.
        '''
        population = self.random_population(self.population_size)
        for n in range(self.num_generations):
            for individual in population:
                fig = copy.deepcopy(self.figure)
                simulation = Simulation(individual.actions, fig, self.sim_runtime)
                simulation.run()
                individual.set_score(simulation.evaluate()) 
            self.evaluate_population(population)
            self.best_individual = population[0]
            population = self.create_next_population(population)  
            print('Generation {}'.format(n + 1))
            print('Best actions: {}'.format(self.best_individual.actions))
            print('Best score: {}\n'.format(int(self.best_individual.score)))