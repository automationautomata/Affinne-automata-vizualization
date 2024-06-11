from PyQt6.QtWidgets import QLabel, QMainWindow, QLineEdit, \
                            QPushButton, QMessageBox, QCheckBox
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from matplotlib import pyplot as plt
from graph import Graph
from widgets import FunctionWidget, WidgetsContainer
from function import LiniarFunction
import pyvistaqt as pvqt
from sys import maxsize

class MainWindow(QMainWindow):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self._setup_ui()
        self.graph = Graph()
        self.app = app
    def _setup_ui(self, label_width = 80, std_height = 30, input_width = 140, 
                  size_width = 600, size_height = 500, func_height = 100, scroll_width = 430):
        # General settings for the window
        self.setWindowTitle("HELLO")
        self.resize(size_width, size_height)
        self.__msgBox__ = QMessageBox()

        self.__points_num_label__ = QLabel(self)
        self.__points_num_label__.setFont(QFont('Arial', 12))
        self.__points_num_label__.setText(" Precision")
        self.__points_num_label__.resize(input_width - 60, std_height)

        self.__input_points_num__ = QLineEdit(self)
        self.__input_points_num__.setFont(QFont('Arial', 15))
        self.__input_points_num__.resize(input_width, std_height)
        self.__input_points_num__.move(input_width - 60, 0)
        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*"))
        self.__input_points_num__.setValidator(valid)

        def __initfunctionWidget__(*args):
            functionWidget = FunctionWidget(index=next(args[0]))
            functionWidget.setFixedSize(args[1]-20, args[2]) 
            functionWidget.setsize(args[3], args[4], args[5])
            functionWidget.setposition(0, 10)
            return functionWidget
        args = (i for i  in range(0, maxsize)), \
               scroll_width, func_height, \
               std_height, label_width, input_width
        self.container = WidgetsContainer(scroll_width, size_height-std_height, 
                                          0, std_height, 
                                          *args, initfunc=__initfunctionWidget__, 
                                          parent=self)
        self.container.addItem()
        self.container.setParent(self)
        
        self.__drawbutton__ = QPushButton(self)
        self.__drawbutton__.setFont(QFont('Arial', 12))
        self.__drawbutton__.setText("Draw")
        self.__drawbutton__.clicked.connect(self.drawclick)
        self.__drawbutton__.move(scroll_width + 20, std_height + 12)
        
        self.__addbutton__ = QPushButton(self)
        self.__addbutton__.setFont(QFont('Arial', 12))
        self.__addbutton__.setText("Add")
        self.__addbutton__.clicked.connect(self.addfunction)
        self.__addbutton__.move(scroll_width + 20, self.__drawbutton__.height()*2 + 12)

        self.show_generalplot = QCheckBox(self)
        self.show_generalplot.setChecked(False)
        self.show_generalplot.move(scroll_width + 20, self.__drawbutton__.height()*3 + 12)
        
        self.__show_generalplot_label__ = QLabel(self)
        self.__show_generalplot_label__.setFont(QFont('Arial', 9))
        self.__show_generalplot_label__.setText("Show general plot")
        self.__show_generalplot_label__.resize(input_width, std_height)
        self.__show_generalplot_label__.move(scroll_width + 35, self.__drawbutton__.height()*3 + 12)

        self.show_separately = QCheckBox(self)
        self.show_separately.setChecked(False)
        self.show_separately.move(scroll_width + 20, self.__drawbutton__.height()*4 + 12)

        self.__show_separately_label__ = QLabel(self)
        self.__show_separately_label__.setFont(QFont('Arial', 9))
        self.__show_separately_label__.setText("Show separately")
        self.__show_separately_label__.resize(input_width, std_height)
        self.__show_separately_label__.move(scroll_width + 35, self.__drawbutton__.height()*4 + 12)
        


    
    def addfunction(self):
        self.container.addItem()

    def __showError__(self, msg):
        self.__msgBox__.setText(msg)
        self.__msgBox__.exec()

    def drawclick(self):
        if self.__input_points_num__.text() != '':
            precision = int(self.__input_points_num__.text())
            if precision < 10:
                self.__showError__("Error: small precision")
                return
        else:
            self.__showError__("Error: enter precision")
            return
        widgets = []
        for functionWidget in self.container.Widgets:
            a, b = functionWidget.getinput()
            if '/' in b and int(b[-1]) % 2 == 0:
                self.__showError__("Error: slope coefficient isn't correct")
            elif '/' in a and int(a[-1]) % 2 == 0:
                self.__showError__("Error: free coefficient isn't correct")
            elif not (a == '' and b == ''):
                widgets.append(functionWidget)
        self.graph.close()
        self.graph.plotter = pvqt.BackgroundPlotter(app=self.app, line_smoothing=True, polygon_smoothing=True)
        self.graph.drawtorus(precision)

        general_plot = None
        if self.show_generalplot.isChecked():
            self.graph.create_plots_generator(len(widgets)+1, self.show_separately.isChecked())
            general_plot = next(self.graph.plots_generator)
            general_plot.set_title("General plot")
            general_plot.set_xlim(self.graph.plot_limits)
            general_plot.set_ylim(self.graph.plot_limits)
            general_plot.grid(True)
        else:
            self.graph.create_plots_generator(len(widgets),  self.show_separately.isChecked())
        for widget in widgets:
            self.draw(widget, precision, general_plot)
        plt.show(block=False)
        plt.tight_layout()
           
    def draw(self, functionWidget, precision, general_plot=None, show=False):
        a, b = functionWidget.getinput()
        if a == '': a = '0' 
        if b == '': b = '0'
        linfunction = LiniarFunction(a, b, precision)
        functionWidget.set_functioninfo(linfunction.info())
        
        colors = self.graph.generatecolors(linfunction.cablenum())
        cables = linfunction.divideoncables()
        self.graph.drawcables(cables, colors)

        comments = []
        for i in range(len(colors)):
            comment = r'$\dfrac{' + str(linfunction.freecoefs[i].numerator)   + r'}' + \
                             r'{' + str(linfunction.freecoefs[i].denominator) + r'}$'
            comments.append(comment)
        title = f"{functionWidget.getname()}{a}x + {b}"
        self.graph.drawlineplot(cables, colors, comments, title, general_plot, show)

