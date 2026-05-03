import random
def initiate_population(pop_size, num_cities):
    population = []
    base_route = list(range(num_cities))
    for i in range(pop_size):
        individual = base_route.copy()
        random.shuffle(individual)
        population.append(individual)
    return population

def calculate_fitness(route, distance_matrix):
    total_distance = 0
    for i in range(len(route)):
        city_a = route[i]
        city_b = route[(i + 1) % len(route)]
        total_distance += distance_matrix[city_a][city_b]
    return total_distance