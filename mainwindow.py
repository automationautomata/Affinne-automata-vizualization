from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, \
                            QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from graphic import Graph
from widgets import FunctionWidget
from function import LiniarFunction
from pyvista import Plotter

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.graph = Graph()


    def _setup_ui(self, label_width = 60, std_height = 30, input_width = 140, size_x = 1000, size_y = 500):
        # General settings for the window
        self.setWindowTitle("PyMAPDL example application")
        self.resize(size_x, size_y)
        self.__msgBox__ = QMessageBox()

        self.__points_num_label__ = QLabel(self)
        self.__points_num_label__.setFont(QFont('Arial', 12))
        self.__points_num_label__.setText(" Precision")
        self.__points_num_label__.resize(input_width - 60, std_height)

        self.__input_points_num__ = QLineEdit(self)
        self.__input_points_num__.setFont(QFont('Arial', 15))
        self.__input_points_num__.resize(input_width, std_height)
        self.__input_points_num__.move(input_width - 60, 0)
        
        self.__layout__ = QVBoxLayout()
        self.__layout__.setContentsMargins(0, 0, 0, 0)

        self.__functionWidget__ = FunctionWidget(self)
        self.__functionWidget__.resize(400, 500) 
        self.__functionWidget__.move(0, std_height) 
        self.__functionWidget__.setsize(std_height, label_width, input_width)
        self.__functionWidget__.setposition(10, 10)
        
        self.__drawbutton__ = QPushButton(self)
        self.__drawbutton__.setFont(QFont('Arial', 12))
        self.__drawbutton__.setText("Draw")
        self.__drawbutton__.clicked.connect(self.onclick)
        self.__drawbutton__.move(self.__functionWidget__.width() + 10 , std_height + 10)

    def onclick(self):
        a, b = self.__functionWidget__.getinput()
        if a == '' or b == '':
            if a == '': a = '0' 
            if b == '': b = '0'
        if self.__input_points_num__.text() == '':
            self.__msgBox__.setText("Error: enter precision")
            self.__msgBox__.exec()
        elif '/' in b and int(b[-1]) % 2 == 0:
            self.__msgBox__.setText("Error: slope coefficient isn't correct")
            self.__msgBox__.exec()
        elif '/' in a and int(a[-1]) % 2 == 0:
            self.__msgBox__.setText("Error: free coefficient isn't correct")
            self.__msgBox__.exec()
        else:
            self.linfunction = LiniarFunction(b, a, int(self.__input_points_num__.text()))
            self.__functionWidget__.set_functioninfo(self.linfunction.info())
            plotter = Plotter()
            if self.graph.plotter:
                self.graph.plotter.close()
            self.graph.drawtorus(plotter, int(self.__input_points_num__.text()))
            colors = self.graph.generatecolors(self.linfunction.cablenum())
            cables = self.linfunction.divideoncables()
            self.graph.drawcables(self.linfunction.divideoncables(), colors)

            comments = []
            for i in range(len(colors)):
                comment = r'$\dfrac{' + str(self.linfunction.freecoefs[i].numerator) + r'}' + \
                                     r'{' + str(self.linfunction.freecoefs[i].denominator) + r'}$'
                comments.append(comment)
            self.graph.drawplot(cables, colors, comments)
            #self.linfunction.divideonlines()
            #data = [line.calc(100) for line in self.linfunction.lines]
            #self.graph.addknot(data)
            self.graph.plotter.show()