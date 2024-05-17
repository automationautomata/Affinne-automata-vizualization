from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget, \
                            QLineEdit, QPushButton, QMessageBox, QScrollArea, QGridLayout
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, Qt
from matplotlib import pyplot as plt
from graphic import Graph
from widgets import FunctionWidget
from function import LiniarFunction
from pyvista import Plotter

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.graph = Graph()

    def _setup_ui(self, label_width = 80, std_height = 30, input_width = 140, 
                  size_x = 1000, size_y = 500, func_height = 50, scroll_width = 415):
        # General settings for the window
        self.setWindowTitle("HELLO")
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
        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*"))
        self.__input_points_num__.setValidator(valid)


        container = QWidget()
        layout = QGridLayout(container)
        functionWidget = FunctionWidget()

        self.__scroll__ = QScrollArea(self)
        self.__scroll__.move(0, std_height)
        self.__scroll__.resize(scroll_width, self.height())
        container.resize(scroll_width, self.height())

        layout.addWidget(functionWidget)
        #container.setLayout(layout)
        self.__scroll__ .setWidget(container)

        layout.setVerticalSpacing(1)
        layout.setColumnStretch(0, 0)

        functionWidget.resize(scroll_width-20, func_height) 
        functionWidget.move(0, 0) 
        functionWidget.setsize(std_height, label_width, input_width)
        functionWidget.setposition(0, 10)
        functionWidget.show()

        self.__drawbutton__ = QPushButton(self)
        self.__drawbutton__.setFont(QFont('Arial', 12))
        self.__drawbutton__.setText("Draw")
        self.__drawbutton__.clicked.connect(self.drawclick)
        self.__drawbutton__.move(scroll_width + 10, std_height + 12)
        
        self.__addbutton__ = QPushButton(self)
        self.__addbutton__.setFont(QFont('Arial', 12))
        self.__addbutton__.setText("Add")
        self.__addbutton__.clicked.connect(self.addfunction)
        self.__addbutton__.move(scroll_width + 10, 
                                self.__drawbutton__.height()*2 + 12)


        # for i in range(10):
        #     for j in range(5):
        #         button = QPushButton(f'{i}x{j}')
        #         layout.addWidget(button, i, j)


    def onquit(self):
        if self.graph.plotter:
            self.graph.plotter.deep_clean()
            self.graph.plotter.close()
        plt.close('all')    
    
    def addfunction(self):
        print(self.dumpObjectTree())
        layoutWidget = self.__scroll__.widget()
        idx = layoutWidget.layout().count()
        last = layoutWidget.layout().itemAt(idx-1).widget()
        print(last.size(), last.size())
        #layoutWidget.resize(layoutWidget.width(), layoutWidget.height() + last.height())

        widget = FunctionWidget(self, index=idx)
        layoutWidget.layout().addWidget(widget)
        #layoutWidget.layout().setColumnStretch(idx, 0)

        layoutWidget.resize(layoutWidget.width(), last.height()) 
        #widget.move(0, last.y()+last.height()) 
        widgetParams = last.widgetParams
        widget.setsize(widgetParams[0], widgetParams[1], widgetParams[2])
        widget.setposition(0, 10)
        print(widget.size(), widget.size())

        #self.__functionWidgets__.append(widget)
        widget.show()

    def drawclick(self):
        layoutWidget = self.__scroll__.widget()
        num = layoutWidget.layout().count()
        for i in range(num):
            functionWidget = layoutWidget.layout().itemAt(i).widget()
            a, b = functionWidget.getinput()
            precision = int(self.__input_points_num__.text())
            if self.__input_points_num__.text() == '':
                self.__msgBox__.setText("Error: enter precision")
                self.__msgBox__.exec()
            elif precision < 10:
                self.__msgBox__.setText("Error: small precision")
                self.__msgBox__.exec()
            elif '/' in b and int(b[-1]) % 2 == 0:
                self.__msgBox__.setText("Error: slope coefficient isn't correct")
                self.__msgBox__.exec()
            elif '/' in a and int(a[-1]) % 2 == 0:
                self.__msgBox__.setText("Error: free coefficient isn't correct")
                self.__msgBox__.exec()
            else:
                self.graph.close()
                if not self.graph.plotter:
                    self.graph.plotter = plotter = Plotter(line_smoothing=True, polygon_smoothing=True)
                self.draw(functionWidget, precision, plotter)
                

    def draw(self, functionWidget, precision):
        a, b = functionWidget.getinput()
        if a == '' or b == '':
            if a == '': a = '0' 
            if b == '': b = '0'
        linfunction = LiniarFunction(b, a, precision)
        functionWidget.set_functioninfo(linfunction.info())
        
        self.graph.drawtorus(self.graph.plotter, precision)
        colors = self.graph.generatecolor(self.linfunction.cablenum())
        cables = linfunction.divideoncables()
        self.graph.drawcables(linfunction.divideoncables(), colors)

        comments = []
        for i in range(len(colors)):
            comment = r'$\dfrac{' + str(linfunction.freecoefs[i].numerator) + r'}' + \
                             r'{' + str(linfunction.freecoefs[i].denominator) + r'}$'
            comments.append(comment)
        self.graph.drawplot(cables, colors, comments)
        #self.linfunction.divideonlines()
        #data = [line.calc(100) for line in self.linfunction.lines]
        #self.graph.addknot(data)
        self.graph.plotter.show(auto_close=True)
    
    # def closeEvent(self, event):
    #     self.graph.close()
    #     event.accept() 