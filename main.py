# import pyvista as pv
# from pyvistaqt import BackgroundPlotter, QtInteractor
# from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
# import sys
# from mainwindow import MainWindow

# #plotter.show()
# # tm = pv.Plotter()
# # tm.show_grid()
# # tm.show()
#  # Только для доступа к аргументам командной строки
# # Приложению нужен один (и только один) экземпляр QApplication.
# # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# # Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
# app = QApplication(sys.argv)
# #tg = TorusGraphic()
# #tg.drawtorus(BackgroundPlotter(app=app))
# #tg.plotter.show()
# # Создаём виджет Qt — окно.
# window = MainWindow()

# # from pyvistaqt import BackgroundPlotter
# # plotter = BackgroundPlotter(toolbar=False, menu_bar=False)
# # plotter.interactor = window
# # _ = plotter.add_mesh(s)
# # #window.resize(600, 400)
# # plotter.enable_point_picking(callback=callback, show_message=True, use_mesh=True, 
# #                                     show_point=True, point_size=10, left_clicking=True)
# # window.setCentralWidget()
# window.show()
# # window.surface.plotter.show()
# app.exec()


# Запускаем цикл событий.
from math import ceil
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from fractions import Fraction
class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        #print('line', x1, y1, x2, y2)
    def calc(self, number):
        x = np.linspace(self.x1, self.x2, number)
        #print('-', self.x1, self.y1, self.x2, self.y2)
        k = (self.y2 - self.y1) / (self.x2 - self.x1)
        b = self.y1 - self.x1*k
        #print("--", k, b)
        y = x*k + b
        return x, y

def func(color, freecoef_2adic, frac):
  slopecoef_2adic = float(frac)
  x = np.linspace(0, 1, 50)
  y = slopecoef_2adic * x + freecoef_2adic
  # plt.grid(True)
  # plt.scatter(x, y,  s = 2)
  # plt.show()
  lines = []
  i = 0
  # fig = plt.figure()
  j = 0
  x = []
  y = []
  x_prev = -freecoef_2adic/slopecoef_2adic
  y_prev = 0
  points = [(x_prev, y_prev)]
  print("---", x_prev, y_prev)
  step = 1
  if slopecoef_2adic < 0:
    step = -1
  x_prev = ceil(x_prev) if x_prev % 1 != 0 else x_prev + 1
  y_prev += 1
  print("---", x_prev, y_prev)
  y_tmp = set()
  for t in range(0, frac.denominator*step, step):
    tmp = t+x_prev
    y_st = freecoef_2adic + slopecoef_2adic*(tmp)
    print(t, 'y', tmp, y_st)
    if y_st % 1 == 0:
      y_tmp.add(y_st)
    points.append((round(tmp, 5), round(y_st , 5)))
  limit = abs(frac.numerator)
  for t in range(0, limit): 
    if t+y_prev not in y_tmp:
      tmp = t+y_prev
      x_st = (tmp - freecoef_2adic)/slopecoef_2adic
      print(t, 'x', round(x_st, 5), round(tmp, 5))
      points.append((round(x_st, 5), round(tmp, 5)))
    else:
      limit+=1
  # print(points)
  # plt.grid(True)

  points = sorted(points, key=lambda vec: ((vec[0] - points[0][0])**2 + (vec[1] - points[0][1])**2)**0.5, reverse=frac.numerator<0)
  print(np.array(points))
  x = []
  y =[]
  # plt.grid(True)
  # plt.scatter([i[0] for i in points], [i[1] for i in points],  s = 2)
  # plt.show()
  mod1 = lambda val: val%1 if val%1 != 0 else 1
  for i in range(1, len(points)):
    if points[i][1] < points[i-1][1]:
      start_y = mod1(points[i-1][1])
      end_y = points[i][1]%1
    else:
      end_y = mod1(points[i][1])
      start_y = points[i-1][1]%1
    start_x = points[i-1][0]%1
    end_x = mod1(points[i][0])
    print(i, ":", start_x, start_y, end_x, end_y)
    lines.append(Line(start_x, start_y, end_x, end_y))
    tx, ty = lines[i-1].calc(10)
    plt.plot(tx, ty, color = color)
  x = np.array(x)
  y = np.array(y)
  data = [line.calc(50) for line in lines]
  x, y = lines[0].calc(10)
# freecoef_2adic = float(Fraction('2/3'))
# frac = Fraction('3/5')
func("green", float(Fraction('2/3')), Fraction('2'))
func("blue", float(Fraction('1/3')), Fraction('2'))
plt.legend()
plt.grid(True)
plt.show()

# import pyvista as pv
# def _toruscoords(vec):
#     global lns, radius, b
#     x = vec[1]*2*np.pi
#     y = vec[0]*2*np.pi

#     # result = y_axe*np.sin(y) + x_axe*np.cos(y)
#     # tmp = np.array(result)
#     # tmp[2] = radius
#     # #mesh = pv.Line(np.array([0, 0, 0]), 2*result)
#     # #lns.add_mesh(mesh, show_edges=True, color=[1.0, 0, 0], line_width=10)  

#     # result = result*2*np.sin(x/2) + z_axe*2*np.cos(x/2)
#     result = np.array([(b+radius*np.cos(x))*np.cos(y),
#                        (b+radius*np.cos(x))*np.sin(y), 
#                        radius*np.sin(x)])
#     #mesh = pv.Line(np.array([0, 0, 0]), z_axe)
#     #lns.add_mesh(mesh, show_edges=True, color=[1.0, 1.0, 0], line_width=10)  
#     # mesh = pv.Line(np.array([0, 0, 0]), result)
#     # lns.add_mesh(mesh, show_edges=True, color=[0.0, 0.0, 1.0], line_width=10)  
#     return result
# radius = 0.5/np.pi
# y_axe = np.array([0, radius, 0])
# z_axe = np.array([0, 0, radius])
# x_axe = np.array([radius, 0, 0])

# plotter = pv.Plotter()
# lns = pv.Plotter()
# lns.show_grid()
# u=np.linspace(-np.pi,np.pi,25)
# v=np.linspace(0,2*np.pi,25)
# u,v=np.meshgrid(u,v)
# a = radius
# b = 1/np.pi
# x = (b + a*np.cos(u)) * np.cos(v)
# y = (b + a*np.cos(u)) * np.sin(v)
# z = a * np.sin(u)
# grid = pv.StructuredGrid(x, y, z)
# # Define a simple linear surface

# plotter.add_mesh(grid, style="surface", show_edges=True,
#                scalar_bar_args={'vertical': True}, color="pink", pickable=True)
# #self.plotter.enable_point_picking(callback=self.__callback, show_message=True, use_mesh=True, 
# #                             show_point=True, point_size=10, left_clicking=True)
# plotter.show_grid()
# plotters = [plotter, pv.Plotter()]

# for t in range(0, len(data)):
#     array = data[t]
#     # start = _toruscoords((array[0][0], array[1][0]))
#     # for i in range(1, min(len(array[0]), len(array[1]))):
#     #     #print(array[0][i-1], array[1][i-1], '|', array[0][i], array[1][i])
#     #     end = _toruscoords((array[0][i], array[1][i]))
#     #     mesh = pv.Line(start, end)
#     #     start = end
#     #     plotter.add_mesh(mesh, show_edges=True, color='k', line_width=10)
#     #     #print("------")
#     y = array[0]*2*np.pi
#     x = array[1]*2*np.pi
#     mesh = pv.Spline(np.column_stack(((b+radius*np.cos(x))*np.cos(y),
#                        (b+radius*np.cos(x))*np.sin(y), 
#                        radius*np.sin(x))))
#     plotter.add_mesh(mesh, show_edges=True, color=[1, 1.0, 0], line_width=10)  

# plotter.show()
# #lns.show()