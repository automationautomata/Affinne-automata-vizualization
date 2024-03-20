from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

class FunctionInput(QWidget):
    def __init__(self, parent=None):
        super(FunctionInput, self).__init__(parent)
        self._label_func = QLabel(self)
        self._label_arg = QLabel(self)
        self._label_func.setFont(QFont('Arial', 15)) 
        self._label_arg.setFont(QFont('Arial', 15)) 

        self._label_func.setText("f(x) = ")
        self._label_arg.setText(" x  +")

        self._input_coef = QLineEdit(self)
        self._input_freecoef = QLineEdit(self)
        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*+/+[1-9][0-9]*"))
        self._input_coef.setValidator(valid)
        self._input_freecoef.setValidator(valid)
        self._input_coef.setFont(QFont('Arial', 15)) 
        self._input_freecoef.setFont(QFont('Arial', 15)) 
 
        super().resize(200, 100) 
        self._setsize(30, 60, 120)
        self._setposition(10, 10, self._label_func.width(), self._input_coef.width())

    def _setposition(self, start_x, start_y, step_label, step_input):
        self._label_func.move(start_x, start_y)
        start_x += step_label
        self._input_coef.move(start_x, start_y)
        start_x += step_input
        self._label_arg.move(start_x, start_y)
        start_x += step_label
        self._input_freecoef.move(start_x, start_y)

    def _setsize(self, height, label_width, input_width):
        self._label_func.resize(label_width, height)
        self._label_arg.resize(label_width, height)
        self._input_coef.resize(input_width, height)
        self._input_freecoef.resize(input_width, height)  

        
    
    