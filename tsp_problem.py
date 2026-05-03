import numpy as np
import tsplib95

class TSPProblem:
    def __init__(self, file_path):
        self.problem = tsplib95.load(file_path)
        self.name = self.problem.name
        self.dimension = self.problem.dimension
        self.weight_type = self.problem.edge_weight_type
        self.dist_matrix = self._create_dist_matrix()

    def _create_dist_matrix(self):
        size = self.dimension
        matrix = np.zeros((size, size))
        nodes = list(self.problem.get_nodes())

        for i in range(size):
            for j in range(size):
                matrix[i, j] = self.problem.get_weight(nodes[i], nodes[j])
        return matrix


