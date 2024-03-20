from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from fractions import Fraction

class LiniarFunction:
    def __init__(self, accuracy, **coefficients):
        self.slopecoef_rat = Fraction(coefficients["slopecoef"])
        self.freecoef_rat = Fraction(coefficients["freecoef"])
        self.slopecoef_2adic = self.fractionTo2adic(self.slopecoef_rat, accuracy)
        self.freecoef_2adic = self.fractionTo2adic(self.freecoef_rat, accuracy)
        return

    def fractionTo2adic(rational, accuracy):
        result = 0b00000000
        numer = rational.numerator
        denom = rational.denominator
        i = 0
        numbers = dict()

        tmp = (numer - denom)/2
        if tmp % 1 == 0:
            result += 1 << i
            numer = tmp
        else: 
            numer /= 2
        i+=1

        while int(numer) not in numbers.keys():
            numbers[int(numer)] = i
            tmp = (numer - denom)/2
            if tmp % 1 == 0:
                result += 1 << i
                numer = tmp
            else: 
                numer /= 2
            i+=1
        cycle = result >> numbers[int(numer)]

        for j in range(i + 1, i + accuracy):
            result += cycle << (j - i) * (i - numbers[int(numer)])
        return result
    
    def calc(self):
        return
class FunctionWidget(QWidget):
    def __init__(self, parent=None):
        super(FunctionWidget, self).__init__(parent)
        
        self._label_func = QLabel(self)
        self._label_arg = QLabel(self)
        self._label_accuracy = QLabel(self)

        self._label_func.setFont(QFont('Arial', 15)) 
        self._label_arg.setFont(QFont('Arial', 15)) 
        self._label_accuracy.setFont(QFont('Arial', 15)) 

        self._label_func.setText("f(x) = ")
        self._label_arg.setText(" x  +")
        self._label_accuracy.setText("Accuracy")

        self._input_accuracy = QLineEdit(self)
        self._input_slopecoef = QLineEdit(self)
        self._input_freecoef = QLineEdit(self)

        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*+/+[1-9][0-9]*"))
        self._input_slopecoef.setValidator(valid)
        self._input_freecoef.setValidator(valid)
        self._input_slopecoef.setFont(QFont('Arial', 15)) 
        self._input_freecoef.setFont(QFont('Arial', 15)) 

        valid = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*"))
        self._input_accuracy.setValidator(valid)
        self._input_accuracy.setFont(QFont('Arial', 15)) 

        super().resize(200, 100) 
        self._setsize(30, 60, 140)
        self._setposition(10, 10, self._label_func.width(), self._input_slopecoef.width())

    def _setposition(self, start_x, start_y, step_label, step_input):
        self._label_accuracy.move(start_x, start_y + self._label_func.height())
        self._input_accuracy.move(start_x + self._label_accuracy.width(), start_y + self._label_func.height())
        self._label_func.move(start_x, start_y)
        start_x += step_label
        self._input_slopecoef.move(start_x, start_y)
        start_x += step_input
        self._label_arg.move(start_x, start_y)
        start_x += step_label
        self._input_freecoef.move(start_x, start_y)

    def _setsize(self, height, label_width, input_width):
        self._label_func.resize(label_width, height)
        self._label_arg.resize(label_width, height)
        self._label_accuracy.resize(label_width + 25, height)
        self._input_slopecoef.resize(input_width, height)
        self._input_freecoef.resize(input_width, height)  
        self._input_accuracy.resize(input_width, height)


        
    
    