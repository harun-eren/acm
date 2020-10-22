import matplotlib.pyplot as plt
from statistics import mean
import pickle

# returns the directory of the sample for given L,F,Q,X,Y,W values
def find_path(l, f, q, x, y, w, metric_name):
    directory = "results/" + str(l) + "/" + str(f) + "_" + str(q) + "/" + str(x) + "_" + str(y) + "_" + str(w)
    path = directory + "/" + metric_name + ".pickle"
    return path

metrics = ['time to stabilize', "is stable", "number of regions", "region sizes",
                         "regions: mean of coordinates", "number of cultures", "culture sizes",
                         "cultures: mean of coordinates"]

## INPUT PARAMETERS
metric_id = 2       # Choose which metrics you wish to observe by its index in the list
metric_name = metrics[metric_id]
l = 40
f = 5
q = 10
x = int(l/2)
W = [0, 2, 4, 6, 10, 20]
Y = [15]
stats = []

path = find_path(l, f, q, int(l/2), 0, 0, metric_name)
metrics_data = pickle.load(open(path,"rb"))
stats.append(mean(metrics_data))

for w in range(len(W)):
    for y in range(len(Y)):
        if not (W[w]==0):
            path = find_path(l, f, q, int(l/2), Y[y], W[w], metric_name)
            metrics_data = pickle.load(open(path,"rb"))
            stats.append(mean(metrics_data))

plt.plot([w/l for w in W], stats, color='green', marker='o', linestyle='dashed',linewidth=1, markersize=10)


plt.title("For L = " + str(l) + " , F = " + str(f) + ", q = " + str(q) + " x = " + str(x) + " y = " + str(Y[0]))
plt.ylabel('Number of Regions')
plt.xlabel('Window Size (w)')
plt.savefig("L" + str(l) + "F" + str(f) + "Q" + str(q) + "X" + str(x) + "Y" + str(Y[0]) + ".png")
plt.show()

