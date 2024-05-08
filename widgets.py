from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, Qt
from function import *

class FunctionWidget(QWidget):
    def __init__(self, parent=None):
        super(FunctionWidget, self).__init__(parent)
        
        self._label_func = QLabel(self)
        self._label_arg = QLabel(self)
        self._label_out = QLabel(self)
        self._label_precision = QLabel(self)

        self._label_func.setFont(QFont('Arial', 15)) 
        self._label_arg.setFont(QFont('Arial', 15)) 
        self._label_precision.setFont(QFont('Arial', 15))
        self._label_out.setFont(QFont('Arial', 15))
        self._label_out.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self._label_func.setText("f(x) = ")
        self._label_arg.setText(" x  +")
        self._label_precision.setText("Precision")

        self._input_precision = QLineEdit(self)
        self._input_slopecoef = QLineEdit(self)
        self._input_freecoef = QLineEdit(self)

        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*+/+[1-9][0-9]*"))
        self._input_slopecoef.setValidator(valid)
        self._input_freecoef.setValidator(valid)
        self._input_slopecoef.setFont(QFont('Arial', 15))
        self._input_freecoef.setFont(QFont('Arial', 15))

        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*"))
        self._input_precision.setValidator(valid)
        self._input_precision.setFont(QFont('Arial', 15)) 

        self._button = QPushButton(self)
        self._button.setFont(QFont('Arial', 12))
        self._button.setText("Draw")
        self.msgBox = QMessageBox()
        self._button.clicked.connect(self.onclick)

    def getinput(self):
        return self._input_freecoef.text(), self._input_slopecoef.text(), self._input_precision.text()
    
    def onclick(self):
        a, b, prec = self.getinput()
        if a == '' or b == '':
            self.msgBox.setText("Error: enter coefficients")
            self.msgBox.exec()
        elif prec == '' and '/' in a and '/' in b:
            self.msgBox.setText("Error: enter precision")
            self.msgBox.exec()
        else:
            self.linearF = LiniarFunction(a, b, int(prec))
            self.linearF.info()
            self._label_out.setText(self.linearF.info())
            self.surface = Torus()
            self.surface.drawtorus(Plotter())
            self.linearF.divideonlines()
            data = [line.calc(100) for line in self.linearF.lines]
            self.surface.addknot(data)
            self.surface.plotter.show()

    def setposition(self, start_x, start_y):
        step_label, step_input = self._label_func.width(), self._input_slopecoef.width()
        self._label_precision.move(start_x, 20 + start_y + self._label_func.height())
        self._input_precision.move(start_x + self._label_precision.width(), 20 + start_y + self._label_func.height())
        self._label_out.move(start_x, 20 + start_y + 2*self._input_precision.height())
        self._label_func.move(start_x, start_y)
        start_x += step_label
        self._input_slopecoef.move(start_x, start_y)
        start_x += step_input
        self._label_arg.move(start_x, start_y)
        start_x += step_label
        self._input_freecoef.move(start_x, start_y)
        start_x += step_input
        self._button.move(start_x, start_y)

    def setsize(self, height, label_width, input_width):
        self._label_func.resize(label_width, height)
        self._label_arg.resize(label_width, height)
        self._label_precision.resize(label_width + 25, height)
        self._label_out.resize(label_width*5, height*4)
        self._input_slopecoef.resize(input_width, height)
        self._input_freecoef.resize(input_width, height)  
        self._input_precision.resize(input_width, height)
        self._button.resize(label_width + 15, height)


        
    
    