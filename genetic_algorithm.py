from operators import *
from utils import initiate_population, calculate_fitness
import random

class GeneticAlgorithm:
    def __init__(
            self,
            distance_matrix,
            pop_size,
            selection_type,
            crossover_type,
            mutation_type,
            elite_size
    ):
        self.matrix = distance_matrix
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.selections = {
            "tournament": tournament_selection,
            "roulette": roulette_selection,
            "rank": rank_selection,
        }
        self.crossovers = {
            "ox": ordered_crossover,
            "pmx": partially_mapped_crossover,
            "erx": edge_recombination_crossover,
        }
        self.mutations = {
            "swap": swap_mutation,
            "inverse": inverse_mutation,
            "scramble": scramble_mutation,
        }
        self.selection_fn = self.selections[selection_type]
        self.crossover_fn = self.crossovers[crossover_type]
        self.mutation_fn = self.mutations[mutation_type]

        num_cities = len(distance_matrix)
        self.population = initiate_population(pop_size, num_cities)
        self.history = []

    def run_generation(self, cx_pb, mut_pb):
        # -- Fitness Scores of generation
        fitness_scores = [
            calculate_fitness(ind, self.matrix) for ind in self.population
        ]

        # -- For charts
        self.history.append(min(fitness_scores))

        # -- Sorting for elitarism
        scored_population = sorted(
            zip(self.population, fitness_scores), key=lambda x: x[1]
        )
        new_population = []
        for i in range(self.elite_size):
            new_population.append(scored_population[i][0].copy())

        # -- Main loop of appending selected/crossed/mutated offsprings to new_population
        while len(new_population) < self.pop_size:

            # -- Selection --
            if self.selection_fn == tournament_selection:
                p1 = self.selection_fn(self.population, 4, fitness_scores)
                p2 = self.selection_fn(self.population, 4, fitness_scores)
            else:
                p1 = self.selection_fn(self.population, fitness_scores)
                p2 = self.selection_fn(self.population, fitness_scores)

            # -- Crossing --
            if random.random() < cx_pb:
                offspring = self.crossover_fn(p1, p2)

                if isinstance(offspring, tuple):
                    c1, c2 = offspring
                else:
                    
                    c1, c2 = offspring, p2.copy()
            else:
                c1, c2 = p1.copy(), p2.copy()

            # -- Mutation --
            if random.random() < mut_pb:
                c1 = self.mutation_fn(c1)
            if random.random() < mut_pb:
                c2 = self.mutation_fn(c2)

            # -- Appending new population --
            new_population.append(c1)
            if len(new_population) < self.pop_size:
                new_population.append(c2)

        self.population = new_population
        return scored_population[0]  # -- Return best from original population
