from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, Qt
from fractions import Fraction
from math import gcd
from numpy import linspace, array
from numpy.linalg import norm
from pyvista import Plotter
from graphic import Torus
class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
    def calc(self, number):
        x = linspace(self.x1, self.x2, number)
        k = (self.y2 - self.y1) / (self.x2 - self.x1)
        b = self.y1 - self.x1*k
        print("--", k, b)
        y = x*k + b
        return x, y
    
class LiniarFunction:
    def __init__(self, slopecoef, freecoef):
        self(slopecoef, freecoef, 0)
        return
    def __init__(self, slopecoef, freecoef, precision):
        self.slopecoef_rat = Fraction(slopecoef)
        self.freecoef_rat = Fraction(freecoef)
        self.slopecoef_2adic = self.fractionTo2adic(self.slopecoef_rat, precision)
        self.freecoef_2adic = self.fractionTo2adic(self.freecoef_rat, precision)
        return
    def fractionTo2adic(self, rational, precision):
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
        if precision > 0 or denom == rational.denominator != 1:
            cycle = result >> numbers[int(numer)]

            for j in range(i + 1, i + precision + 1):
                result += cycle << (j - i) * (i - numbers[int(numer)] + 1)
        return result
    
    def divideonlines(self):  
        self.lines =[]
        freecoef = float(self.freecoef_rat)
        slopecoef = float(self.slopecoef_rat)
        x_prev = freecoef/slopecoef
        y_prev = slopecoef*x_prev + freecoef
        points = [(x_prev, y_prev)]
        x_prev += 1
        y_prev += 1
        num = self.knotnum()

        for t in range(0, num*(self.slopecoef_rat.denominator - 1)):
          y_st = freecoef + slopecoef*(t+x_prev)
          tmp = (y_st - freecoef)/slopecoef
          points.append((tmp, y_st))
        for t in range(0, num*(self.slopecoef_rat.numerator)):
          x_st = (t+y_prev - freecoef)/slopecoef
          tmp = slopecoef*x_st + freecoef
          points.append((x_st, tmp))
        points = sorted(points, key=lambda vec: (vec[0]**2 + vec[1]**2)**0.5)
        mod1 = lambda val: val%1 if val%1 != 0 else 1
        for i in range(1, len(points)):
          self.lines.append(Line(points[i-1][0]%1, points[i-1][1]%1, mod1(points[i][0]), mod1(points[i][1])))
        return
    def multiplicativeOrder(self, A, N) :
        if (gcd(A, N ) != 1) :
            return -1
        # result store power of A that raised 
        # to the power N-1
        result = 1
        K = 1
        while (K < N) :
            # modular arithmetic
            result = (result * A) % N 
            # return smallest + ve integer
            if (result == 1) :
                return K
            # increment power
            K = K + 1
        return -1
    def knotnum(self):
        e = gcd(self.freecoef_rat.denominator, self.slopecoef_rat.denominator)
        return self.multiplicativeOrder(2, int(self.freecoef_rat.denominator/e))
    def info(self):
        numbers_info = f"{self.freecoef_rat} = {bin(self.freecoef_2adic)} = {self.freecoef_2adic}\
                        \n{self.slopecoef_rat} = {bin(self.slopecoef_2adic)} = {self.slopecoef_2adic}"
        knot_info = f"number of knots: {self.knotnum()}\n" #knot turns around the inner circle: {}"
        return f"{numbers_info}\n\n{knot_info}"

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


        
    
    