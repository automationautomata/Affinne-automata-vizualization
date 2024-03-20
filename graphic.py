import numpy as np
from numpy.linalg import norm
import pyvista as pv
from vg import angle

class TorusGraphic:
    radius = 0.5/np.pi
    y_normal = np.array([0, radius, 0])
    z_normal = np.array([0, 0, radius])
    def __planecoords(self, vec):
        proj = vec - (np.dot(vec, self.z_normal)/norm(self.z_normal)**2)*self.z_normal
        proj *= self.radius/norm(proj)
        a_y = angle(proj, self.y_normal) 
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
        # Define a simple linear surface
  
        self.plotter.add_mesh(self.grid, scalars=self.grid.points[:, -1], show_edges=True,
                        scalar_bar_args={'vertical': True}, pickable=True)
        self.plotter.enable_point_picking(callback=self.__callback, show_message=True, use_mesh=True, 
                                    show_point=True, point_size=10, left_clicking=True)
        self.plotter.show_grid()