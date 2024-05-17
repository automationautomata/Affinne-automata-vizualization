from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, Qt

class FunctionWidget(QWidget):
    small= {'0':'₀', '1':'₁', '2':'₂', '3':'₃', '4':'₄', '5':'₅', '6':'₆', '7':'₇', '8':'₈', '9':'₉'}
    def __init__(self, parent=None, index=0):
        super(FunctionWidget, self).__init__(parent)
        
        self.__label_func__ = QLabel(self)
        self.__label_arg__ = QLabel(self)
        self.__function_info__ = QLabel(self)

        self.__label_func__.setFont(QFont('Arial', 15)) 
        self.__label_arg__.setFont(QFont('Arial', 15)) 
        self.__function_info__.setFont(QFont('Arial', 10))
        self.__function_info__.setTextInteractionFlags(Qt.TextSelectableByMouse)

        smallindex = ''.join([self.small[s] for s in str(index)])
        self.__label_func__.setText(f"f{smallindex}(x) = ")
        self.__label_arg__.setText("x  +")

        self.__input_slopecoef__ = QLineEdit(self)
        self.__input_freecoef__ = QLineEdit(self)

        valid = QRegularExpressionValidator(QRegularExpression("(-|0|)[1-9][0-9]*+/+[1-9][0-9]*"))
        self.__input_slopecoef__.setValidator(valid)
        valid = QRegularExpressionValidator(QRegularExpression("(-|0|)[1-9][0-9]*+/+[1-9][0-9]*"))
        self.__input_freecoef__.setValidator(valid)
        self.__input_slopecoef__.setFont(QFont('Arial', 15))
        self.__input_freecoef__.setFont(QFont('Arial', 15))

    def getinput(self):
        return self.__input_freecoef__.text(), self.__input_slopecoef__.text()
    def getindex(self):
        return self.__label_func__.text()
    
    def setposition(self, start_x, start_y):
        step_input = self.__input_slopecoef__.width()
        self.__function_info__.move(start_x, 20 + start_y + 2*self.__input_slopecoef__.height())
        self.__label_func__.move(start_x, start_y)
        start_x += self.__label_func__.width()
        self.__input_slopecoef__.move(start_x, start_y)
        start_x += step_input
        self.__label_arg__.move(start_x, start_y)
        start_x += self.__label_arg__.width()
        self.__input_freecoef__.move(start_x, start_y)
        start_x += step_input

    def setsize(self, height, label_width, input_width):
        self.widgetParams = height, label_width, input_width
        self.__label_func__.resize(label_width, height)
        self.__label_arg__.resize(label_width-40, height)
        self.__function_info__.resize(self.width(), height*2)
        self.__input_slopecoef__.resize(input_width, height)
        self.__input_freecoef__.resize(input_width, height)  

    def set_functioninfo(self, info):
        self.__function_info__.setText(info)

#FunctionWidget