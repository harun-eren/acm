import simulation, visualization




def main():
    # define L, F, q, x, y, w and k
    L = 10
    F = 10
    q = 5
    x = 1
    y = 0
    w = 1
    step_number = 1000
    num_of_realization = 1
    acm_simulator = simulation.Simulation(L, F, q)
    acm_simulator.run([x,y,w], step_number, num_of_realization)
    # acm_visualize = visualization.Visualization(L, F, acm_simulator.data)
    # acm_visualize.run()

if __name__== "__main__":
  main()