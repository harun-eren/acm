import random


# Simulation constraints
# L is even number (assumption)
# 0 <= x <= L/2
# 0 <= w <= L
# 0 <= y
# if w <= L/2 then 0 <= w+y <= L/2
# else y = 0

class Simulation:
    L = 0  # length of one size, where population size is LxL
    F = 0  # number of features per an individual
    q = 0  # number of traits per feature
    x = 0  # length of obstacle, where x <= L/2
    y = 0  # location of window
    w = 0  # window size, where 0 <= w <=L
    population = []  # population

    def __init__(self, L, F, q):
        self.L = L
        self.F = F
        self.q = q

    # initializes the population based on L,F,q
    def initialize_population(self):
        ppl = []
        for i in range(self.L):
            row = []
            for j in range(self.L):
                indv = []
                for feature in range(self.F):
                    indv.append(random.randint(1,self.q))
                row.append(indv)
            ppl.append(row)
        self.population = ppl

    # get neighbors that the given indv can interact, based on its location
    def get_neighbors(self, indv_i, indv_j):
        neighbors = []
        if indv_j > 0:
            neighbors.append(self.population[indv_i][indv_j - 1])

        if indv_j < (self.L - 1):
            neighbors.append(self.population[indv_i][indv_j + 1])

        if indv_i > 0:
            if indv_i == self.x:
                if self.y + self.w > indv_j >= self.y:
                    neighbors.append(self.population[indv_i - 1][indv_j])
            else:
                neighbors.append(self.population[indv_i - 1][indv_j])
        if indv_i < (self.L - 1):
            if indv_i == (self.x - 1):
                if self.y + self.w > indv_j >= self.y:
                    neighbors.append(self.population[indv_i + 1][indv_j])
            else:
                neighbors.append(self.population[indv_i + 1][indv_j])
        print(self.x)
        return neighbors

    # indv1 interacts with indv2, depending on similarity between them
    def interact(self, indv1, indv2):
        r = random.random()
        similarity = 0
        different_traits = []
        is_equal = True

        for i in range(len(indv1)):
            if indv1[i] == indv2[i]:
                similarity += 1 / self.F
            else:
                is_equal = False
                different_traits.append(i)

        if r < similarity < 1 and not is_equal:
            rtrait = random.choice(different_traits)  # a randomly selected trait among different traits between neighbors
            indv1[rtrait] = indv2[rtrait]
        return indv1

    def run(self, params, step_number):
        data = []
        self.x = params[0]
        self.y = params[1]
        self.w = params[2]

        for sample in range(5):
            self.initialize_population()
            for step in range(step_number):
                i = random.randint(0, self.L-1)
                j = random.randint(0,self.L-1)
                neighbors = self.get_neighbors(i, j)
                r_neighbor = random.choice(neighbors)
                self.population[i][j] = self.interact(self.population[i][j], r_neighbor)
            data.append(self.population)
        return data
