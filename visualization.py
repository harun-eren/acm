import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import simulation
from tkinter import Tk, Canvas

class Visualization():


    size = 620
    edge = 10

    def __init__(self, L, F, obstacle, data):
        self.L = L
        self.F = F
        self.data = data[0]
        self.grid_width = (self.size - 2 * self.edge) / self.L
        self.obstacle = obstacle
        print(self.grid_width)
        self.line_width = self.grid_width / 5

    def calculate_dissimilarity(self, loc, direction):
        i = loc[0]
        j = loc[1]
        indv1 = self.data[j][i]
        indv2 = []
        dissimilarity = 0
        print(i," and ",j)
        if direction == "right":
            indv2 = self.data[j][i+1]
        elif direction == "down":
            indv2 = self.data[j+1][i]

        for i in range(len(indv1)):
            if indv1[i] != indv2[i]:
                dissimilarity += 1 / self.F
        return dissimilarity

    def rectangle(self, c, loc, direction):
        dissimilarity = self.calculate_dissimilarity(loc, direction)
        x = loc[0] * self.grid_width
        y = loc[1] * self.grid_width

        if dissimilarity > 0:
            # right wall
            if direction == "right":
                c.create_line(self.edge + x + self.grid_width, self.edge + y,
                              self.edge + x + self.grid_width, self.edge + y + self.grid_width,
                              width=self.line_width*dissimilarity)
            # down wall
            if direction == "down":
                c.create_line(self.edge + x, self.edge + y + self.grid_width,
                              self.edge + x + self.grid_width, self.edge + y + self.grid_width,
                              width=self.line_width*dissimilarity)

    def run(self):
        root = Tk()
        root.geometry('700x700')
        c = Canvas(root, height=680, width=680)

        c.create_line(self.edge, self.edge,
                      self.edge, self.edge + self.L * self.grid_width, width=self.line_width)
        c.create_line(self.edge, self.edge,
                      self.edge + self.L * self.grid_width, self.edge, width=self.line_width)
        c.create_line(self.edge + self.L * self.grid_width, self.edge,
                      self.edge + self.L * self.grid_width, self.edge + self.L * self.grid_width, width=self.line_width)
        c.create_line(self.edge, self.edge + self.L * self.grid_width,
                      self.edge + self.L * self.grid_width, self.edge + self.L * self.grid_width, width=self.line_width)

        for i in range(self.L):
            for j in range(self.L):
                if j != self.L-1:
                    self.rectangle(c, [i,j], "down")
                if i != self.L-1:
                    self.rectangle(c, [i, j], "right")
        c.create_line(self.edge + self.obstacle[0]*self.grid_width, self.edge,
                      self.edge + self.obstacle[0]*self.grid_width, self.edge + self.obstacle[1]*self.grid_width,
                      width=0, fill="blue")
        c.create_line(self.edge + self.obstacle[0] * self.grid_width, self.edge + (self.obstacle[1] + self.obstacle[2])*self.grid_width,
                      self.edge + self.obstacle[0] * self.grid_width, self.edge + self.L*self.grid_width,
                      width=0, fill="blue")
        c.pack()
        root.mainloop()