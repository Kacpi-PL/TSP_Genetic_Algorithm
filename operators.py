import random


def tournament_selection(population, tournament_size, fitness):
    participants_indexes = random.sample(range(len(population)), tournament_size)

    parent_index = participants_indexes[0]

    for index in participants_indexes:
        if fitness[index] < fitness[parent_index]:
            parent_index = index

    return population[parent_index].copy()


def roulette_selection(population, fitness):
    inverted_fitness = [1.0 / d for d in fitness]
    total_fitness = sum(inverted_fitness)
    pick = random.uniform(0, total_fitness)
    current_sum = 0

    for index in range(len(population)):
        current_sum += inverted_fitness[index]
        if current_sum > pick:
            return population[index].copy()


def rank_selection(population, fitness):
    ranked = sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)
    total_ranks = sum(range(1, len(population) + 1))
    pick = random.uniform(0, total_ranks)
    current_sum = 0
    for i in range(len(ranked)):
        rank = i + 1
        current_sum += rank
        if current_sum > pick:
            return list(ranked[i][0])


def ordered_crossover(parent1, parent2):
    size = len(parent1)
    point1, point2 = random.sample(range(size), 2)
    offspring1 = []
    offspring2 = []
    start = min(point1, point2)
    stop = max(point1, point2)
    offspring1 = [None] * size
    offspring2 = [None] * size
    offspring1[start:stop] = parent1[start:stop]
    offspring2[start:stop] = parent2[start:stop]
    parent1_ordered = parent1[stop:] + parent1[:stop]
    parent2_ordered = parent2[stop:] + parent2[:stop]
    genes_for_offspring1 = [
        gene for gene in parent2_ordered if gene not in offspring1[start:stop]
    ]
    genes_for_offspring2 = [
        gene for gene in parent1_ordered if gene not in offspring2[start:stop]
    ]
    index = stop
    for gene in genes_for_offspring1:
        if index >= size:
            index = 0
        offspring1[index] = gene
        index += 1

    index = stop
    for gene in genes_for_offspring2:
        if index >= size:
            index = 0
        offspring2[index] = gene
        index += 1

    return offspring1, offspring2


def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    point1, point2 = random.sample(range(size), 2)
    offspring1 = []
    offspring2 = []
    start = min(point1, point2)
    stop = max(point1, point2)
    offspring1 = [None] * size
    offspring2 = [None] * size
    offspring1[start:stop] = parent1[start:stop]
    offspring2[start:stop] = parent2[start:stop]
    for i in range(start, stop):
        if parent2[i] not in offspring1[start:stop]:
            current_gene = parent2[i]
            index = i
            while start <= index < stop:
                gene_in_parent1 = parent1[index]
                index = parent2.index(gene_in_parent1)
            offspring1[index] = current_gene

    for i in range(start, stop):
        if parent1[i] not in offspring2[start:stop]:
            current_gene = parent1[i]
            index = i
            while start <= index < stop:
                gene_in_parent2 = parent2[index]
                index = parent1.index(gene_in_parent2)
            offspring2[index] = current_gene

    for i in range(size):
        if offspring1[i] is None:
            offspring1[i] = parent2[i]
        if offspring2[i] is None:
            offspring2[i] = parent1[i]

    return offspring1, offspring2


def edge_recombination_crossover(parent1, parent2):
    size = len(parent1)

    edge_map = {city: set() for city in parent1}

    for i in range(size):
        c1, c2 = parent1[i], parent2[i]

        edge_map[c1].add(parent1[i - 1])
        edge_map[c1].add(parent1[(i + 1) % size])

        edge_map[c2].add(parent2[i - 1])
        edge_map[c2].add(parent2[(i + 1) % size])

    offspring = []

    unvisited = set(parent1)

    current_city = random.choice([parent1[0], parent2[0]])

    while len(offspring) < size:
        offspring.append(current_city)
        unvisited.remove(current_city)

        if not unvisited:
            break

        current_neighbors = edge_map[current_city]

        for neighbor in current_neighbors:
            if current_city in edge_map[neighbor]:
                edge_map[neighbor].remove(current_city)

        if current_neighbors:
            min_len = 5
            best_candidates = []

            for neighbor in current_neighbors:
                n_len = len(edge_map[neighbor])
                if n_len < min_len:
                    min_len = n_len
                    best_candidates = [neighbor]
                elif n_len == min_len:
                    best_candidates.append(neighbor)

            current_city = random.choice(best_candidates)
        else:
            current_city = random.choice(tuple(unvisited))

    return offspring


def swap_mutation(offspring):
    point1, point2 = random.sample(range(len(offspring)), 2)
    offspring_after_mutation = offspring.copy()
    offspring_after_mutation[point1], offspring_after_mutation[point2] = (
        offspring_after_mutation[point2],
        offspring_after_mutation[point1],
    )
    return offspring_after_mutation


def inverse_mutation(offspring):
    point1, point2 = random.sample(range(len(offspring)), 2)
    start = min(point1, point2)
    stop = max(point1, point2)
    offspring_after_mutation = offspring.copy()
    offspring_after_mutation[start: stop + 1] = offspring_after_mutation[
        start: stop + 1
    ][::-1]
    return offspring_after_mutation


def scramble_mutation(offspring):
    point1, point2 = random.sample(range(len(offspring)), 2)
    start = min(point1, point2)
    stop = max(point1, point2)
    offspring_after_mutation = offspring.copy()
    fragment = offspring_after_mutation[start: stop + 1]
    random.shuffle(fragment)
    offspring_after_mutation[start: stop + 1] = fragment
    return offspring_after_mutation
