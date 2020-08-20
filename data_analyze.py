import pickle
L = 10
F = 5
q = 10
x = 5
y = 5
w = 5
directory = "results"
directory += ("/" + str(L))
directory += ("/" + str(F) + "_" + str(q))
directory += ("/" + str(x) + "_" + str(y) + "_" + str(w))
maps = pickle.load(open(directory+"/maps.pickle","rb"))
is_stable = pickle.load(open(directory+"/is stable.pickle","rb"))
number_o_regs = pickle.load(open(directory+"/number of regions.pickle","rb"))
number_o_cultures = pickle.load(open(directory+"/number of cultures.pickle","rb"))
reg_sizes = pickle.load(open(directory+"/region sizes.pickle","rb"))
time = pickle.load(open(directory+"/time to stabilize.pickle","rb"))
mean_coord = pickle.load(open(directory+"/regions: mean of coordinates.pickle","rb"))

print(maps)
print(is_stable)
print(number_o_regs)
print(number_o_cultures)
print(reg_sizes)
print(mean_coord)
print(time)
