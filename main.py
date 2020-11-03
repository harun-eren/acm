import simulation, grid_visualization, math


def main():
    # define the variables L, F, q, x, y, w and k
    # L: length of one side of the square area
    # F: number of cultural features
    # q: number of possible traits for each feature
    # x: horizontal position of obstacle,
    # y: vertical position of the beginning of the window on the obstacle
    # w: size of the window

    L = [8]
    F = [5]
    Q = [10, 15]
    x = [int(l / 2) for l in L]
    num_of_realization = 10
    step_number = [100000 * l * l for l in L]
    Y = [0,1,2,3]
    W = [1,3,5,7]

    # in case of multiple values, run the simulations for each value of each variable
    for f in F:
        for q in Q:
            for i in range(len(L)):
                for y in Y:
                    for w in W:
                        if y <= int(math.ceil((L[i] - w )/ 2)):
                            #print(L[i]," ", f," ", q," ", x[i]," ", y," ", w)
                            acm_simulator = simulation.Simulation(L[i], f, q, visualize_grid=False)
                            acm_simulator.run([x[i], y, w], step_number[i], num_of_realization)


if __name__ == "__main__":
    main()
