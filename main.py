import simulation, grid_visualization, math


def main():
    # define L, F, q, x, y, w and k
    # L : size, F: feature number, q: possible property number
    # x: position of obstacle, y: position of window, w: window size

    L = [8]
    F = [5]
    Q = [10, 15]
    x = [int(l / 2) for l in L]
    num_of_realization = 10
    step_number = [100000 * l * l for l in L]
    Y = [0,1,2,3]
    W = [1,3,5,7]

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
