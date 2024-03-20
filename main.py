import pyvista as pv
from pyvistaqt import BackgroundPlotter
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from widgets import FunctionWidget
from graphic import TorusGraphic
import sys

#plotter.show()
# tm = pv.Plotter()
# tm.show_grid()
# tm.show()
 # Только для доступа к аргументам командной строки
# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)
f = FunctionWidget()
sphere = pv.Sphere()
tg = TorusGraphic()
tg.drawtorus(BackgroundPlotter(app=app))
#tg.plotter.show()
# Создаём виджет Qt — окно.
window = QMainWindow()
window.resize(600, 400)
window.setCentralWidget(f)
window.show()  # Важно: окно по умолчанию скрыто.

# Запускаем цикл событий.
app.exec()