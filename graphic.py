import numpy as np
from numpy.linalg import norm
import pyvista as pv
from vg import angle

class Torus:
    radius = 0.5/np.pi
    y_axe = np.array([0, radius, 0])
    z_axe = np.array([0, 0, radius])
    x_axe = np.array([radius, 0, 0])
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
    def _toruscoords(self, vec):
        x = vec[0]*2*np.pi
        y = vec[1]*2*np.pi

        # result = y_axe*np.sin(y) + x_axe*np.cos(y)
        # tmp = np.array(result)
        # tmp[2] = radius
        # #mesh = pv.Line(np.array([0, 0, 0]), 2*result)
        # #lns.add_mesh(mesh, show_edges=True, color=[1.0, 0, 0], line_width=10)  

        # result = result*2*np.sin(x/2) + z_axe*2*np.cos(x/2)
        result = np.array([ (self.radius+self.radius*np.cos(x))*np.cos(y),
                            (self.radius+self.radius*np.cos(x))*np.sin(y), 
                            self.radius*np.sin(x)])
        #mesh = pv.Line(np.array([0, 0, 0]), z_axe)
        #lns.add_mesh(mesh, show_edges=True, color=[1.0, 1.0, 0], line_width=10)  
        # mesh = pv.Line(np.array([0, 0, 0]), result)
        # lns.add_mesh(mesh, show_edges=True, color=[0.0, 0.0, 1.0], line_width=10)         
        return result
    # Create and plot structured grid
    def drawtorus(self, pltr):
        self.plotter = pltr
        self.lp = None 

        u=np.linspace(-np.pi,np.pi,25)
        v=np.linspace(0,2*np.pi,25)
        u,v=np.meshgrid(u,v)
        a = self.radius
        b = 0.5/np.pi
        x = (b + a*np.cos(u)) * np.cos(v)
        y = (b + a*np.cos(u)) * np.sin(v)
        z = a * np.sin(u)
        self.grid = pv.StructuredGrid(x, y, z)
        self.plotter.add_mesh(self.grid, style="wireframe", show_edges=True,
               scalar_bar_args={'vertical': True}, color="k", pickable=True)

        # Define a simple linear surface
  
        # self.plotter.add_mesh(self.grid, scalars=self.grid.points[:, -1], show_edges=True,
        #                 scalar_bar_args={'vertical': True}, pickable=True)
        self.plotter.enable_point_picking(callback=self.__callback, show_message=True, use_mesh=True, 
                                    show_point=True, point_size=10, left_clicking=True)
        self.plotter.show_grid()
    def addknot(self, data):
        for array in data:
            start = self._toruscoords((array[0][0], array[1][0]))
            for i in range(1, min(len(array[0]), len(array[1]))):
                end = self._toruscoords((array[0][i], array[1][i]))
                mesh = pv.Line(start, end)
                start = end
                self.plotter.add_mesh(mesh, show_edges=True, color=[1, 1.0, 0], line_width=10)  
        return