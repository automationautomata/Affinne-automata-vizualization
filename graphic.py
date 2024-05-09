import numpy as np
from numpy.linalg import norm
import pyvista as pv
from vg import angle
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class Graph:
    major_radius = 1/np.pi
    minor_radius = 0.5/np.pi
    y_axe = np.array([0, major_radius, 0])
    z_axe = np.array([0, 0, minor_radius])
    x_axe = np.array([minor_radius, 0, 0])
    def __init__(self):
        self.plotter = None
        pass
    def __planecoords(self, vec):
        proj = vec - (np.dot(vec, self.z_axe)/norm(self.z_axe)**2)*self.z_axe
        proj *= self.radius/norm(proj)
        a_y = angle(proj, self.y_axe) 
        if proj[1] < 0:
            a_y = 360 - a_y
        a_x = angle(vec - proj, proj)
        if vec[2] < 0:
            a_x = 360 - a_x    
        return a_x/360, a_y/360
    
    def __callback(self, mesh, pid):
        if self.lp:
            self.plotter.remove_actor(lp)
        point = self.grid.points[pid]
        label = [f'ID: {pid}\n: {self.__planecoords(point)}\n {point}']
        lp = self.plotter.add_point_labels(point, label, name="label")
    
    def __toruscoords__(self, *args):
        x = args[0]*2*np.pi
        y = args[1]*2*np.pi
        a = self.minor_radius
        b = self.major_radius
        return (b+a*np.cos(x))*np.cos(y), \
               (b+a*np.cos(x))*np.sin(y), \
                a*np.sin(x)
    
    # Create and plot structured grid
    def drawtorus(self, plotter, precision):
        self.plotter = plotter
        self.lp = None 

        u=np.linspace(-np.pi,np.pi,precision)
        v=np.linspace(0,2*np.pi,precision)
        u,v=np.meshgrid(u,v)
        a = self.minor_radius
        b = self.major_radius
        x = (b + a*np.cos(u)) * np.cos(v)
        y = (b + a*np.cos(u)) * np.sin(v)
        z = a * np.sin(u)
        self.plotter.add_mesh(pv.StructuredGrid(x, y, z), style="surface", show_edges=True,
               scalar_bar_args={'vertical': True}, color="pink", pickable=True)

        # Define a simple linear surface
  
        # self.plotter.add_mesh(self.grid, scalars=self.grid.points[:, -1], show_edges=True,
        #                 scalar_bar_args={'vertical': True}, pickable=True)
        # self.plotter.enable_point_picking(callback=self.__callback, show_message=True, use_mesh=True, 
        #                             show_point=True, point_size=10, left_clicking=True)
        self.plotter.show_grid()
    def generatecolors(self, number):
        colors = []
        for i in range(number):
            colors.append([ np.round(np.random.rand(),1),
                            np.round(np.random.rand(),1),
                            np.round(np.random.rand(),1), 
                            np.round(np.clip(np.random.rand(), 0, 1), 1) ])
        return colors
    def drawcable(self, cable, color):
        for t in range(len(cable)):
            # array = data[t]
            # start = _toruscoords((array[0][0], array[1][0]))
            # for i in range(1, min(len(array[0]), len(array[1]))):
            #     #print(array[0][i-1], array[1][i-1], '|', array[0][i], array[1][i])
            #     end = _toruscoords((array[0][i], array[1][i]))
            #     mesh = pv.Line(start, end)
            #     start = end
            #     plotter.add_mesh(mesh, show_edges=True, color='k', line_width=10)
            #     #print("------")
            # y = array[0]*2*np.pi
            # x = array[1]*2*np.pi
            points = self.__toruscoords__(cable[t][1], cable[t][0])
            mesh = pv.Spline(np.column_stack(points))
            self.plotter.add_mesh(mesh, show_edges=True, color=color, line_width=10)  

    def drawcables(self, cables, colors):
        for i in range(len(cables)):
            self.drawcable(cables[i], colors[i])
        #self.plotter.show() 

    def drawplot(self, cables, colors, comments):
        legend = []
        for i in range(len(cables)):
            for line in cables[i]:
                plt.plot(line[0], line[1], color=colors[i][:3])
            legend.append(Line2D([0], [0], color=colors[i][:3], lw=4, label=comments[i]))
        #_, ax = plt.subplots()
        plt.legend(handles=legend, loc='upper right', framealpha=0.2)
        plt.grid(True)
        plt.show(block=False)