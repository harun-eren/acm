import random
import grid_visualization
import pickle
from pathlib import Path


# Simulation constraints
# L is an even number (assumption)
# 0 <= x <= L/2
# 0 <= w <= L
# 0 <= y <= ceiling ((L-w) / 2)

class Simulation:
    L = 0                   # length of one side, where population size is LxL
    F = 0                   # number of cultural features per an individual
    q = 0                   # number of possible traits per feature
    x = 0                   # horizontal starting position of the obstacle, where x <= L/2
    y = 0                   # vertical starting position of the window on the obstacle
    w = 0                   # size of the window, where 0 <= w <=L
    num_of_realization = 1  # how many times the experiment should be realized
    population = []         # population
    maps = []

    # the metrics by which a simulation will be evaluated
    metrics_name_list = ['time to stabilize', "is stable", "number of regions", "region sizes",
                         "regions: mean of coordinates", "number of cultures", "culture sizes",
                         "cultures: mean of coordinates"]
    metrics = {}
    data = []
    channels = 0
    is_stable = False
    available_neighbors = []

    def __init__(self, L, F, q, visualize_grid):
        self.L = L
        self.F = F
        self.q = q
        self.visualize_grid = visualize_grid
        for metrics_name in self.metrics_name_list:
            self.metrics[metrics_name] = []

    # initializes the population based on the values for L,F,q
    def initialize_population(self):
        # the entire grid of population...
        ppl = []
        for j in range(self.L):
            # ... is made up of rows...
            row = []
            for i in range(self.L):
                # ... of cells of individuals
                indv = []
                for feature in range(self.F):
                    # initialize each feature of an individual
                    # with a random value between 1 and q, which is
                    # the number of possible traits
                    indv.append(random.randint(1, self.q))
                row.append(indv)
            ppl.append(row)
        self.population = ppl
        # initialize the evaluation metrics in the dictionary
        for metrics_name in self.metrics_name_list:
            self.metrics.update({metrics_name: []})

    # returns if it has neighbor (not edge or obstacle) in each side of an indv in given address
    def neighbor_availability(self, j, i):
        up = down = left = right = False

        if j > 0:  # upward neighbor exists
            up = True

        if j < (self.L - 1):  # downward neighbor exists
            down = True

        if i > 0:  # leftward neighbor exists
            left = True
            # if it is next to obstacle, check if it is next to window
            if i == self.x:
                left = self.y + self.w > j >= self.y

        if i < (self.L - 1):  # rightward neighbor exists
            right = True
            # if it is next to obstacle, check if it is next to window
            if i == (self.x - 1):
                right = self.y + self.w > j >= self.y
        return [up, down, left, right]

    # sets the available neighbors for every individual cell on the map
    def set_available_neighbors(self):
        data = []
        for j in range(self.L):
            row = []
            for i in range(self.L):
                local_available_neighbors = []
                neighbor_available = self.neighbor_availability(j, i)
                if neighbor_available[0]:
                    local_available_neighbors.append([j - 1, i])
                if neighbor_available[1]:
                    local_available_neighbors.append([j + 1, i])
                if neighbor_available[2]:
                    local_available_neighbors.append([j, i - 1])
                if neighbor_available[3]:
                    local_available_neighbors.append([j, i + 1])
                row.append(local_available_neighbors)
            data.append(row)
        self.available_neighbors = data

    #
    # # gets available neighbors with which the given indv can interact (not edge or obstacle)
    # def get_available_neighbors_by_culture(self, indv_j, indv_i):
    #     neighbors_culture = []
    #     neighbors_status = self.neighbor_availability(indv_j, indv_i)
    #
    #     if neighbors_status[0]:  # upward neighbor
    #         neighbors_culture.append(self.population[indv_j - 1][indv_i])
    #
    #     if neighbors_status[1]:  # downward neighbor
    #         neighbors_culture.append(self.population[indv_j + 1][indv_i])
    #
    #     if neighbors_status[2]:  # leftward neighbor
    #         neighbors_culture.append(self.population[indv_j][indv_i - 1])
    #
    #     if neighbors_status[3]:  # rightward neighbor
    #         neighbors_culture.append(self.population[indv_j][indv_i + 1])
    #     return neighbors_culture

    # given the feature vectors of two different individuals as input,
    # returns similarity as percentage, list of different traits and boolean is_equal
    def check_similarity_between_indvs(self, indv1, indv2):
        similarity = 0
        different_traits = []
        is_equal = True
        for i in range(len(indv1)):
            if indv1[i] == indv2[i]:
                similarity += 1 / self.F
            else:
                is_equal = False    # if there exists at least one different trait, they are not equal
                different_traits.append(i)
        if is_equal:
            similarity = 1.0
        return similarity, different_traits

    # given the feature vectors of two individuals
    # checks whether there exists a "channel" between the two, that is,
    # whether the two can interact and influence each other:
    # the two must share at least one common trait in one of their features
    # and must not be exactly equal in all features
    def check_if_channel_between_indvs(self, indv1, indv2):
        if indv1 != indv2:
            for feature_i, feature_j in zip(indv1, indv2):
                if feature_i == feature_j:
                    return True
        return False

    # returns the number of channels in the initial map
    def initialize_channel_num(self):
        channels = 0
        for i in range(self.L):
            for j in range(self.L):
                indv = self.population[j][i]
                up, _, left, _ = self.neighbor_availability(j, i)
                if up:  # checks if there is a channel with the upward neighbor
                    if self.check_if_channel_between_indvs(indv, self.population[j - 1][i]):
                        channels += 1
                if left:  # checks if there is a channel with the leftward neighbor
                    if self.check_if_channel_between_indvs(indv, self.population[j][i - 1]):
                        channels += 1
        self.channels = channels

    # returns the number of channels that a given individual has
    def count_local_channels(self, indv, neighbors):
        local_channels = 0
        for neighbor in neighbors:
            if self.check_if_channel_between_indvs(indv, neighbor):
                local_channels += 1
        return local_channels

    # given the address of an individual on the map
    # individual interacts with a randomly selected neighbor
    # with probability depending on the similarity between them
    def interact(self, indv_j, indv_i):
        # choose one of the neighbors randomly from the list of neighbors
        r = random.random()
        indv = self.population[indv_j][indv_i]
        neighbors = [self.population[j][i] for [j, i] in self.available_neighbors[indv_j][indv_i]]
        r_neighbor = random.choice(neighbors)

        # decrement the count of channels by local channels, since it can change by interaction
        self.channels -= self.count_local_channels(indv, neighbors)

        # interaction occurs if random number is less than similarity
        # simulating the probability aspect in the model
        similarity, different_traits = self.check_similarity_between_indvs(indv, r_neighbor)
        if r < similarity < 1:
            rtrait = random.choice(
                different_traits)  # a randomly selected trait among different traits between neighbors
            indv[rtrait] = r_neighbor[rtrait]

        # increment the count of channels by local channels to update the count of channels
        self.channels += self.count_local_channels(indv, neighbors)
        return indv  # returns final state of individual after the interaction

    # identifies the "regions" in the map, that is,
    # the sets of adjacent individuals which are exactly equal in features
    def identify_regions(self):
        regions = []  # stores list of addresses of every individual for each region
        current_region = []
        unvisited = [[True for i in range(self.L)] for j in range(self.L)]
        unvisited_indvs = [[y, x] for x in range(self.L) for y in range(self.L)]
        primary = []
        secondary = []
        primary.append([0, 0])

        while unvisited_indvs or current_region:
            if primary:
                [j, i] = primary.pop()  # pop an individual from the current region
                indv_culture = self.population[j][i]
                if not unvisited[j][i]: # check if visited
                    continue

                try:
                    while True:
                        secondary.remove([j, i])    # attempt to remove the current individual from secondary
                except ValueError:
                    pass

                neighbors = self.available_neighbors[j][i]
                for [y, x] in neighbors:    # check all neighbors of the current individual
                    if unvisited[y][x]:
                        if indv_culture == self.population[y][x]:
                            if [y, x] not in primary:
                                primary.append([y, x])  # add the neighbor to primary if the cultures are equal
                        else:
                            if [y, x] not in secondary:
                                secondary.append([y, x])    # else, add it to secondary

                unvisited[j][i] = False
                unvisited_indvs.remove([j, i])
                current_region.append([j, i])
                # print(j," ",i)
                # print(unvisited_indvs)
            else:
                if secondary:
                    [j, i] = secondary[0]
                    try:
                        while True:
                            secondary.remove([j, i])
                    except ValueError:
                        pass
                    if unvisited[j][i]:
                        regions.append(current_region)
                        current_region = []
                        primary.append([j, i])
                else:
                    if unvisited_indvs:
                        primary.append(unvisited_indvs[0])
                if current_region:
                    regions.append(current_region)
                    current_region = []
        return regions

    def identify_cultures(self):
        cultures = {}  # dict: a distinct feature vector -> addresses of individuals having the same feature vector
        culture_set = set()  # set: set of distinct feature vectors

        for i in range(self.L):
            for j in range(self.L):
                indv = tuple(self.population[j][i])
                if indv not in culture_set:
                    culture_set.add(indv)
                    # temp = ((j, i),)
                    temp = [[j, i]]
                else:
                    # temp = cultures[indv] + ((j, i),)
                    temp = cultures[indv]
                    temp.append([j, i])
                cultures.update({indv: temp})
        return list(cultures.values())

    def analyze_group_of_indvs(self, group):
        subgroup_size_list = []
        subgroup_mean_coordinate_list = []

        for subgroup in group:
            subgroup_size = len(subgroup)
            subgroup_size_list.append(subgroup_size / (self.L * self.L) * 100)
            mean_coordinates = [0, 0]
            for indv_address in subgroup:
                mean_coordinates[0] += indv_address[0] / subgroup_size
                mean_coordinates[1] += indv_address[1] / subgroup_size
            subgroup_mean_coordinate_list.append(mean_coordinates)
        return subgroup_size_list, subgroup_mean_coordinate_list

    def process_data(self):
        # goes to directory in form "./results/L/F_q/x_y_w"
        directory = "results"
        directory += ("/" + str(self.L))
        directory += ("/" + str(self.F) + "_" + str(self.q))
        directory += ("/" + str(self.x) + "_" + str(self.y) + "_" + str(self.w))

        Path(directory).mkdir(parents=True, exist_ok=True)

        with open(directory + "/maps.pickle", 'wb') as f:
            pickle.dump(self.maps, f, pickle.HIGHEST_PROTOCOL)

        for metrics_name in self.metrics_name_list:
            with open(directory + "/" + metrics_name + ".pickle", 'wb') as f:
                pickle.dump(self.metrics[metrics_name], f, pickle.HIGHEST_PROTOCOL)

    # takes in all the input values and runs the simulation
    def run(self, params, step_number, num_of_realization):
        data = []
        self.x = params[0]
        self.y = params[1]
        self.w = params[2]
        self.num_of_realization = num_of_realization
        sample_metrics = [[] for x in range(len(self.metrics_name_list))]

        for sample in range(self.num_of_realization):
            print("size: ", self.L, " ", "f: ", self.F, " q: ", self.q, " | ", sample + 1, " realization")
            self.initialize_population()
            self.initialize_channel_num()
            print(self.channels)
            self.set_available_neighbors()
            stable = False
            timestamp = 0
            for step in range(step_number):
                i = random.randint(0, self.L - 1)
                j = random.randint(0, self.L - 1)
                self.population[j][i] = self.interact(j, i)
                timestamp += 1
                if timestamp % 10000000 == 0:
                    print(timestamp)
                    print(self.channels)
                if self.channels == 0:
                    stable = True
                    break
            print("Mechanism has ended. Statistical calculations start")
            self.regions = self.identify_regions()
            self.cultures = self.identify_cultures()
            regions_size_list, regions_mean_of_coordinates = self.analyze_group_of_indvs(self.regions)
            cultures_size_list, cultures_mean_of_coordinates = self.analyze_group_of_indvs(self.cultures)
            self.maps.append(self.population)

            sample_metrics[0].append(timestamp)  # "time to stabilize"
            sample_metrics[1].append(self.channels == 0)  # "is stable"
            sample_metrics[2].append(len(self.regions))  # "number of regions"
            sample_metrics[3].append(regions_size_list)  # "region sizes"
            sample_metrics[4].append(regions_mean_of_coordinates)  # "regions: mean of coordinates"
            sample_metrics[5].append(len(self.cultures))  # "number of cultures"
            sample_metrics[6].append(cultures_size_list)  # "culture sizes"
            sample_metrics[7].append(cultures_mean_of_coordinates)  # "cultures: mean of coordinates"

            for m_index in range(len(self.metrics_name_list)):
                self.metrics.update({self.metrics_name_list[m_index]: sample_metrics[m_index]})

        if self.visualize_grid:
            image = grid_visualization.Grid_Visualization(self.L, self.F, [self.x, self.y, self.w], self.maps[0])
            image.run()
        self.process_data()
