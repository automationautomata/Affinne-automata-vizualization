from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QScrollArea
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, Qt

class FunctionWidget(QWidget):
    small = {'0':'₀', '1':'₁', '2':'₂', '3':'₃', '4':'₄', '5':'₅', '6':'₆', '7':'₇', '8':'₈', '9':'₉'}
    def __init__(self, parent=None, index=0):
        super(FunctionWidget, self).__init__(parent)

        self.__label_func__ = QLabel(self)
        self.__label_arg__ = QLabel(self)
        self.__function_info__ = QLabel(self)

        self.__label_func__.setFont(QFont('Arial', 15)) 
        self.__label_arg__.setFont(QFont('Arial', 15)) 
        self.__function_info__.setFont(QFont('Arial', 12))
        self.__function_info__.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

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
        return self.__input_slopecoef__.text(), self.__input_freecoef__.text()
    
    def getname(self):
        return self.__label_func__.text()
    
    def setposition(self, start_x, start_y):
        step_input = self.__input_slopecoef__.width()
        self.__function_info__.move(start_x, start_y + self.__input_slopecoef__.height())
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

class WidgetsContainer(QWidget):
    def __init__(self, width, height, pos_x, pos_y, *args, initfunc, parent=None):
        super(WidgetsContainer, self).__init__(parent)
        self.setParent(parent)
        self.move(pos_x, pos_y)
        self.Widgets = []
        self.container = QWidget(self)
        self.__scroll__ = QScrollArea(self)
        self.__scroll__.resize(width, height)
        self.__scroll__.setWidget(self.container)
        self.__scroll__.setParent(self)
        self.__scroll__.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.__scroll__.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.container.resize(width + self.__scroll__.verticalScrollBar().width(), height)
        self.resize(width + self.__scroll__.verticalScrollBar().width(), height)

        self.iteminitfunc = initfunc
        self.itemargs = args

    def showwidget(self):
        self.container.show()
        self.__scroll__.show()
        self.show()
    
    def setItemInit(self, initfunc):
        self.iteminitfunc = initfunc
    
    def setItemArgs(self, *args):
        self.itemargs = args
    
    def addItem(self):
        if self.iteminitfunc: 
            item = self.iteminitfunc(*self.itemargs)
            item.setParent(self.container)
            if len(self.Widgets)*item.height()*2 > self.container.height():
                self.container.resize(self.container.width(), self.container.height()+item.height())

            if len(self.Widgets) != 0:
                item.move(0, self.Widgets[-1].y()+self.Widgets[-1].height())
            else: item.move(0, 0)        
            self.Widgets.append(item)
            item.show()
            


