import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from decimal import Decimal, getcontext
import re
import math

from_class = uic.loadUiType("Calculator.ui")[0]
class WindowClass(QMainWindow, from_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Calculator")
        self.flag = False
        # Connect number buttons (0-9) to a common function
        for i in range(10):
            button = getattr(self, f"pushButton_{i}")
            button.clicked.connect(self.button_Clicked)
        
        self.pushButton_plus.clicked.connect(self.button_Clicked)
        self.pushButton_minus.clicked.connect(self.button_Clicked)
        self.pushButton_mul.clicked.connect(self.button_Clicked)
        self.pushButton_div.clicked.connect(self.button_Clicked)
        self.pushButton_dot.clicked.connect(self.button_Clicked)
        self.pushButton_equal.clicked.connect(self.calculation)
        self.pushButton_pi.clicked.connect(self.button_Clicked)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_mod.clicked.connect(self.mod_button_Clicked)
        self.pushButton_root.clicked.connect(self.button_Clicked)

    def button_Clicked(self):
        sender = self.sender()
        new_text = sender.text()
        current_text = self.lineEdit.text()
        if new_text in ('+', '-', '×', '÷', 'mod'):
            self.flag = False       
            self.lineEdit.setText(current_text + new_text)
        elif self.lineEdit.text() == 'Malformed expression':
            self.lineEdit.setText(new_text) 
        elif self.flag == True:
            self.lineEdit.setText(new_text)
            self.flag = False
        else:
            self.lineEdit.setText(current_text + new_text)

    def mod_button_Clicked(self):
        sender = self.sender()
        current_text = self.lineEdit.text()
        new_text = sender.text()
        self.lineEdit.setText(current_text + ' ' + new_text + ' ')
        self.flag = False
    
    def calculation(self):
        text = self.lineEdit.text()
        if text == '𝛑':
            text = text.replace('𝛑', '3.141592654')
            self.lineEdit.setText(text)
            self.flag = True
            return 0
        # elif text.endswith('𝛑'):
        #     text = text[:-1] + '×3.141592654'
            
        if text[-1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '𝛑'):
            cal_line = self.lineEdit.text()
            cal_line = cal_line.replace('𝛑', '×3.141592654')
            tokens = re.findall(r'\d+\.\d+|\d+|\+|-|×|÷| mod |√\d+|\√\d+\.\d+', cal_line)
            for i in range(len(tokens)):
                if tokens[i][0] == '√':
                    sqrt_result = math.sqrt(float(tokens[i][1:]))
                    tokens[i] = '{:.9g}'.format(sqrt_result)
                                        
            # 숫자와 연산자를 각각의 리스트에 분리
            numbers = [Decimal(token) for token in tokens if token not in ('+', '-', '×', '÷', ' mod ')] 
            operators = [token for token in tokens if token in ['+', '-', '×', '÷', ' mod ']]
            
            # 설정된 정밀도 변경
            precision = 10  # 정밀도를 필요에 따라 조정
            getcontext().prec = precision
            
            result = numbers[0]
            for i in range(len(operators)):
                if operators[i] == '+':
                    result += numbers[i+1]
                elif operators[i] == '-':
                    result -= numbers[i+1]
                elif operators[i] == '×':
                    result *= numbers[i+1]
                elif operators[i] == '÷':
                    result /= numbers[i+1]
                elif operators[i] == ' mod ':
                    result %= numbers[i+1]
            if result == int(result):
                result = int(result)    
            self.lineEdit.setText(str(result)) 
            self.flag = True       
        else:
            self.lineEdit.setText('Malformed expression')
            self.flag = True 
            
    def clear(self):
        self.lineEdit.setText('')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())