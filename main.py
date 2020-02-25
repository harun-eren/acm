import simulation
import numpy as np

def main():
    # define L, F, q, x, y, w and k
    L = 3
    F = 10
    q = 5
    x = 1
    y = 0
    w = 0
    k = 10000
    acm_simulator = simulation.Simulation(L, F, q)
    data = acm_simulator.run([x,y,w], k)
    for result in data:
        print(np.array(result))
        print("\n\n")
    # acm_simulator.initialize_population()
    # a = acm_simulator.get_neighbors(0,0)
    # print(a)

if __name__== "__main__":
  main()