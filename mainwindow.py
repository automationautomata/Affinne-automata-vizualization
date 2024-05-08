from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, \
                            QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from graphic import Torus
from widgets import FunctionWidget, LiniarFunction
from pyvista import Plotter

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self, label_width = 60, std_height = 30, input_width = 140, size_x = 1000, size_y = 500):
        # General settings for the window
        self.setWindowTitle("PyMAPDL example application")
        self.resize(size_x, size_y)
        
        self._points_num_label = QLabel(self)
        self._points_num_label.setFont(QFont('Arial', 12))
        self._points_num_label.setText("Surface precision")
        self._points_num_label.resize(input_width, std_height)

        self._input_points_num = QLineEdit(self)
        self._input_points_num.setFont(QFont('Arial', 15))
        self._input_points_num.resize(input_width, std_height)
        self._input_points_num.move(input_width, 0)
        
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._functionWidget = FunctionWidget(self)
        self._functionWidget.resize(500, 500) 
        self._functionWidget.move(0, std_height) 
        self._functionWidget.setsize(std_height, label_width, input_width)
        self._functionWidget.setposition(10, 10)
        
        self.__drawbutton__ = QPushButton(self)
        self.__drawbutton__.setFont(QFont('Arial', 12))
        self.__drawbutton__.setText("Draw")
        self.msgBox = QMessageBox()
        self.__drawbutton__.clicked.connect(self.onclick)

    def onclick(self):
        a, b, prec = self._functionWidget.getinput()
        if a == '' or b == '':
            self.msgBox.setText("Error: enter coefficients")
            self.msgBox.exec()
        elif prec == '' and '/' in a and '/' in b:
            self.msgBox.setText("Error: enter precision")
            self.msgBox.exec()
        else:
            self.linearFunction = LiniarFunction(a, b, int(prec))
            self.linearFunction.info()
            self._label_out.setText(self.linearFunction.info())
            self.surface = Torus()
            self.surface.drawtorus(Plotter())
            self.linearFunction.divideonlines()
            data = [line.calc(100) for line in self.linearFunction.lines]
            #self.surface.addknot(data)
            self.surface.plotter.show()