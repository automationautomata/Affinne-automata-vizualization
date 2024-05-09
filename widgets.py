from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, Qt

class FunctionWidget(QWidget):
    def __init__(self, parent=None):
        super(FunctionWidget, self).__init__(parent)
        
        self.__label_func__ = QLabel(self)
        self.__label_arg__ = QLabel(self)
        self.__function_info__ = QLabel(self)

        self.__label_func__.setFont(QFont('Arial', 15)) 
        self.__label_arg__.setFont(QFont('Arial', 15)) 
        self.__function_info__.setFont(QFont('Arial', 15))
        self.__function_info__.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.__label_func__.setText("f(x) = ")
        self.__label_arg__.setText(" x  +")

        self.__input_slopecoef__ = QLineEdit(self)
        self.__input_freecoef__ = QLineEdit(self)

        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*+/+[1-9][0-9]*"))
        self.__input_slopecoef__.setValidator(valid)
        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*+/+[1-9][0-9]*"))
        self.__input_freecoef__.setValidator(valid)
        self.__input_slopecoef__.setFont(QFont('Arial', 15))
        self.__input_freecoef__.setFont(QFont('Arial', 15))

    def getinput(self):
        return self.__input_freecoef__.text(), self.__input_slopecoef__.text()

    def setposition(self, start_x, start_y):
        step_label, step_input = self.__label_func__.width(), self.__input_slopecoef__.width()
        self.__function_info__.move(start_x, 20 + start_y + 2*self.__input_slopecoef__.height())
        self.__label_func__.move(start_x, start_y)
        start_x += step_label
        self.__input_slopecoef__.move(start_x, start_y)
        start_x += step_input
        self.__label_arg__.move(start_x, start_y)
        start_x += step_label
        self.__input_freecoef__.move(start_x, start_y)
        start_x += step_input

    def setsize(self, height, label_width, input_width):
        self.__label_func__.resize(label_width, height)
        self.__label_arg__.resize(label_width, height)
        self.__function_info__.resize(label_width*5, height*4)
        self.__input_slopecoef__.resize(input_width, height)
        self.__input_freecoef__.resize(input_width, height)  

    def set_functioninfo(self, info):
        self.__function_info__.setText(info)
