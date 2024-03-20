import pyvista as pv
from pyvistaqt import BackgroundPlotter
import numpy as np
from numpy.linalg import norm
from math import pi
from vg import angle
y_ax = np.array([0, 0.5/np.pi, 0])
z_ax = np.array([0, 0, 0.5/np.pi])
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from widgets import FunctionInput
import sys
def planecoords(vec):
    global y_ax, z_ax, a
    proj = vec - (np.dot(vec, z_ax)/norm(z_ax)**2)*z_ax
    proj *= a/norm(proj)
    # mesh = pv.Line(np.array([0, 0, 0]), proj)
    # tm.add_mesh(mesh, color="k", line_width=10)
    # mesh = pv.Line(np.array([0, 0, 0]), vec - proj)
    # tm.add_mesh(mesh, color="green", line_width=10)
    a_y = angle(proj, y_ax)
    if proj[1] < 0:
        a_y = 360 - a_y
    a_x = angle(vec - proj, proj)
    if vec[2] < 0:
        a_x = 360 - a_x    
    return a_x/360, a_y/360
    #signed_angle(vec, ax1), signed_angle(ax2, zero)

# Define a simple linear surface
u=np.linspace(-np.pi,np.pi,25)
v=np.linspace(0,2*np.pi,25)

u,v=np.meshgrid(u,v)
a = 0.5/np.pi
b = 0.5/np.pi
x = (b + a*np.cos(u)) * np.cos(v)
y = (b + a*np.cos(u)) * np.sin(v)
z = a * np.sin(u)

lp = None 
mesh = None
def callback(mesh, pid):
    global lp
    if lp:
        plotter.remove_actor(lp)
    point = grid.points[pid]
    label = [f'ID: {pid}\n: {planecoords(point)}\n {point}']
    lp = plotter.add_point_labels(point, label, name="label")
# Create and plot structured grid
grid = pv.StructuredGrid(x, y, z)
plotter = BackgroundPlotter() #pv.Plotter()
plotter.add_mesh(grid, scalars=grid.points[:, -1], show_edges=True,
                 scalar_bar_args={'vertical': True}, pickable=True)
plotter.enable_point_picking(callback=callback, show_message=True, use_mesh=True, 
                             show_point=True, point_size=10, left_clicking=True)
plotter.show_grid()
#plotter.show()
# tm = pv.Plotter()
# tm.show_grid()
# tm.show()
 # Только для доступа к аргументам командной строки
# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)
f = FunctionInput()
sphere = pv.Sphere()

plotter = BackgroundPlotter()
plotter.add_mesh(sphere)
# Создаём виджет Qt — окно.
window = QMainWindow()
window.resize(600, 400)
window.setCentralWidget(plotter)
window.show()  # Важно: окно по умолчанию скрыто.

# Запускаем цикл событий.
app.exec()