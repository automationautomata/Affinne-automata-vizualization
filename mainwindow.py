from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget, \
                            QLineEdit, QPushButton, QMessageBox, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, Qt
from matplotlib import pyplot as plt
from graphic import Graph
from widgets import FunctionWidget, WidgetsContainer
from function import LiniarFunction
from pyvista import Plotter
from sys import maxsize
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.graph = Graph()

    def _setup_ui(self, label_width = 80, std_height = 30, input_width = 140, 
                  size_width = 1000, size_height = 500, func_height = 100, scroll_width = 430):
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
            #width, height, std_height, label_width, input_width = args
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
        
        #functionWidget = FunctionWidget()
        #self.functionWidgets = [functionWidget]
        # functionWidget.setFixedSize(scroll_width-20, func_height) 
        # functionWidget.move(0, 0) 
        # functionWidget.setsize(std_height, label_width, input_width)
        # functionWidget.setposition(0, 10)
        # functionWidget.show()
        # WidgetsContainer()
        # self.__scroll__ = QScrollArea(self)
        # self.__scroll__.move(0, std_height)
        # self.__scroll__.resize(scroll_width + 20, size_height-std_height)
        # container.resize(scroll_width, size_height-std_height)
        # #layout.addWidget(functionWidget)
        # #container.setLayout(layout)
        # self.__scroll__.setWidget(container)
        # container.show()
        # # layout.setVerticalSpacing(1)
        # layout.addStretch(12)
        # layout.addSpacing(50)
        # layout.setContentsMargins(0, 0, 0, 0)
        # # Create a horizontal spacer item
        # spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding , QSizePolicy.Policy.Fixed)

        # # Add the spacer item to the layout
        # layout.addItem(spacer)

        
        self.__drawbutton__ = QPushButton(self)
        self.__drawbutton__.setFont(QFont('Arial', 12))
        self.__drawbutton__.setText("Draw")
        self.__drawbutton__.clicked.connect(self.drawclick)
        self.__drawbutton__.move(scroll_width + 20, std_height + 12)
        
        self.__addbutton__ = QPushButton(self)
        self.__addbutton__.setFont(QFont('Arial', 12))
        self.__addbutton__.setText("Add")
        self.__addbutton__.clicked.connect(self.addfunction)
        self.__addbutton__.move(scroll_width + 20, 
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
        #print(self.dumpObjectTree())
        self.container.addItem()
        # layoutWidget = self.__scroll__.widget()

        # last = self.functionWidgets[-1]
        # widget = FunctionWidget(parent=layoutWidget, index=len(self.functionWidgets))

        # if len(self.functionWidgets)%3 == 2:
        #    layoutWidget.resize(layoutWidget.width(), layoutWidget.height() + last.height()) 

        # widgetParams = last.widgetParams
        # widget.setsize(widgetParams[0], widgetParams[1], widgetParams[2])
        # widget.setposition(0, 10)
        # widget.setFixedSize(last.size())

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
        self.graph.close()
        self.graph.plotter = Plotter(line_smoothing=True, polygon_smoothing=True)
        self.graph.drawtorus(precision)
        self.graph.setplotsnum(len(self.container.Widgets))
        for functionWidget in self.container.Widgets:
            a, b = functionWidget.getinput()
            if '/' in b and int(b[-1]) % 2 == 0:
                self.__showError__("Error: slope coefficient isn't correct")
            elif '/' in a and int(a[-1]) % 2 == 0:
                self.__showError__("Error: free coefficient isn't correct")
            else:
                self.draw(functionWidget, precision)#plotter)
        plt.show(block=False)
        self.graph.plotter.show()#auto_close=True)


                

    def draw(self, functionWidget, precision):
        a, b = functionWidget.getinput()
        if a == '': a = '0' 
        if b == '': b = '0'
        linfunction = LiniarFunction(b, a, precision)
        functionWidget.set_functioninfo(linfunction.info())
        
        #self.graph.drawtorus(precision)
        colors = self.graph.generatecolors(linfunction.cablenum())
        cables = linfunction.divideoncables()
        self.graph.drawcables(cables, colors)

        comments = []
        for i in range(len(colors)):
            comment = r'$\dfrac{' + str(linfunction.freecoefs[i].numerator)   + r'}' + \
                             r'{' + str(linfunction.freecoefs[i].denominator) + r'}$'
            comments.append(comment)
        self.graph.drawlineplot(cables, colors, comments, "")
         
    def close(self):
        self.graph.close()
        return super().close()