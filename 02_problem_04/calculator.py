import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.engine = CalculatorEngine()
        self.init_ui()

    def init_ui(self):
        self.formula_display = QLineEdit(readOnly=True)
        self.formula_display.setAlignment(Qt.AlignRight)
        self.formula_display.setFont(QFont('맑은 고딕'))
        self.formula_display.setStyleSheet('font-size: 18px; color: #AAAAAA; border: none; padding-right: 10px; background-color: #000000;')
        self.formula_display.setFixedHeight(60)

        self.result_display = QLineEdit('0', readOnly=True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setFont(QFont('맑은 고딕'))
        self.result_display.setStyleSheet('font-size: 80px; color: white; border: none; padding-right: 5px;')
        self.result_display.setFixedHeight(100)

        main_layout = QVBoxLayout()
        button_layout = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                button = QPushButton(btn_text)
                button.setFont(QFont('맑은 고딕'))

                if btn_text == '0':
                    button.setFixedSize(260, 120)
                else:
                    button.setFixedSize(120, 120)

                self.set_button_style(button, btn_text)
                button.clicked.connect(lambda _, text=btn_text: self.on_button_click(text))

                if btn_text == '0':
                    button_layout.addWidget(button, row_idx + 1, 0, 1, 2)
                else:
                    offset = 1 if row_idx == 4 and col_idx >= 1 else 0
                    button_layout.addWidget(button, row_idx + 1, col_idx + offset)

        main_layout.addWidget(self.formula_display)
        main_layout.addWidget(self.result_display)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.setWindowTitle('Calculator')
        self.setFixedSize(600, 900)
        self.setStyleSheet('background-color: #000000')

    def on_button_click(self, text):
        result, formula = self.engine.input(text)
        self.result_display.setText(str(result))
        if formula:
            self.formula_display.setText(formula)
        elif text == 'AC':
            self.formula_display.clear()
        self.adjust_font_size()

    def set_button_style(self, button, text):
        style = "font-size: 36px; border-radius: 60%;"
        if text in ['÷', 'x', '-', '+', '=']:
            style += "background-color: #F6A000; color: white;"
        elif text in ['AC', '+/-', '%']:
            style += "background-color: #AFAFAF; color: black;"
        else:
            style += "background-color: #393939; color: #CDCDCD;"
        button.setStyleSheet(style)

    def adjust_font_size(self):
        text = self.result_display.text()
        length = len(text)
        if length <= 12:
            font_size = 80
        elif length <= 16:
            font_size = 60
        elif length <= 25:
            font_size = 40
        else:
            font_size = 20
        self.result_display.setStyleSheet(f'font-size: {font_size}px; color: white; border: none; padding-right: 5px; background-color: #000000;')

class CalculatorEngine:
    def __init__(self):
        self.expression = ''
        self.waiting_for_new_input = False

    def input(self, text):
        if text == 'AC':
            self.reset()
            return '0', ''
        elif text == '+/-':
            self.negative_positive()
            return self.expression, ''
        elif text == '%':
            self.percent()
            return self.expression, ''
        elif text == '.':
            self.add_decimal()
            return self.expression, ''
        elif text in ['+', '-', 'x', '÷']:
            self.add_operator(text)
            return self.expression, ''
        elif text == '=':
            result = self.equal()
            return result, self.expression
        else:  # 숫자
            if self.waiting_for_new_input:
                self.expression = ''
                self.waiting_for_new_input = False
            self.expression += text
            return self.expression, ''

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return a / b

    def reset(self):
        self.expression = ''
        self.waiting_for_new_input = False

    def negative_positive(self):
        if not self.expression: # 수식이 비어 있으면 무시
            return
        
        i = len(self.expression) - 1 # 수식의 마지막 문자부터 시작해서 거꾸로 탐색
        last_number = '' # 마지막 숫자를 저장할 문자열
        while i >= 0 and (self.expression[i].isdigit() or self.expression[i] == '.'):
            last_number = self.expression[i] + last_number
            i -= 1 # 숫자 또는 소수점을 거꾸로 읽어가며 마지막 숫자 추출
        if i >= 0 and self.expression[i] == '-' and (i == 0 or self.expression[i - 1] in '+-x÷'):
            last_number = '-' + last_number
            i -= 1 # 음수 기호 처리
        if not last_number:
            return # 마지막 숫자를 찾지 못하면 무시
        if last_number.startswith('-'):
            new_number = last_number[1:] # 음수를 양수로 변경
        else:
            new_number = '-' + last_number # 양수를 음수로 변경
        self.expression = self.expression[:i + 1] + new_number # 이전 수식을 변경된 값으로 변경

    def percent(self):
        if not self.expression:
            return

        # 덧셈/뺄셈인 경우: A+B% → A + (A * B / 100)
        for op in reversed(['+', '-']):
            if op in self.expression:
                a, b = self.expression.rsplit(op, 1)
                try:
                    a_val = float(a)
                    b_val = float(b)
                    percent_val = a_val * b_val / 100
                    self.expression = f'{a}{op}{percent_val}'
                    return
                except:
                    self.expression = 'Error'
                    return

        # 곱셈/나눗셈인 경우: 그냥 마지막 숫자를 100으로 나눔
        for op in reversed(['x', '÷']):
            if op in self.expression:
                a, b = self.expression.rsplit(op, 1)
                try:
                    b_val = float(b) / 100
                    self.expression = f'{a}{op}{b_val}'
                    return
                except:
                    self.expression = 'Error'
                    return

        # 수식 전체가 숫자일 경우 단독 %
        try:
            val = float(self.expression)
            self.expression = str(round(val / 100, 6))
        except:
            self.expression = 'Error'

    def add_decimal(self):
        if not self.expression or self.expression[-1] in '+-x÷':
            self.expression += '0.'
        elif '.' not in self._get_last_number():
            self.expression += '.'

    def add_operator(self, operator):
        if self.expression:
            if self.expression[-1] in '+-x÷':
                self.expression = self.expression[:-1] + operator
            else:
                self.expression += operator
            self.waiting_for_new_input = False

    def equal(self):
        tokens = [] # 연산자와 숫자를 저장할 리스트
        num = '' # 현재 처리 중인 숫자
        i = 0 # 인덱스 초기화

        while i < len(self.expression):
            ch = self.expression[i] # 현재 문자

            if ch in '+-x÷': # 연산자인 경우
                if ch == '-' and (i == 0 or self.expression[i - 1] in '+-x÷'):
                    num += ch # 부호로 사용된 -는 숫자에 포함
                else:
                    if num == '':
                        self.expression = 'Error'
                        return 'Error'
                    tokens.append(num) # 숫자 저장
                    tokens.append(ch) # 연산자 저장
                    num = '' # 숫자 초기화
            else:
                num += ch # 숫자에 문자 추가
            i += 1 # 다음 문자로 이동

        if num:
            tokens.append(num) # 마지막 숫자 추가

        if not tokens or tokens[0] in '+-x÷':
            self.expression = 'Error' # 수식이 잘못된 경우
            return 'Error'

        try:
            i = 0
            while i < len(tokens): # x, / 먼저 계산
                if tokens[i] == 'x' or tokens[i] == '÷':
                    left = float(tokens[i - 1]) # 왼쪽 숫자
                    right = float(tokens[i + 1]) # 오른쪽 숫자
                    result = self.multiply(left, right) if tokens[i] == 'x' else self.divide(left, right)
                    tokens[i - 1:i + 2] = [str(result)] # 슬라이스 할당를 사용하여 리스트에서 연산된 부분을 한번에 결과값으로 치환
                    i -= 1 # 인덱스를 한칸 뒤로
                else:
                    i += 1

            result = float(tokens[0]) # 초기값 설정
            i = 1
            while i < len(tokens): # +, - 계산
                op = tokens[i]
                val = float(tokens[i + 1])
                if op == '+':
                    result = self.add(result, val)
                elif op == '-':
                    result = self.subtract(result, val)
                i += 2

            if isinstance(result, float):
                result = round(result, 6) # 소수점 6자리 반올림
            if isinstance(result, float) and result.is_integer():
                result = int(result) # 정수면 정수로 표시

            self.expression = str(result) # 수식 갱신
            self.waiting_for_new_input = True # 다음 입력 대기 설정
            return str(result)

        except ZeroDivisionError:
            self.expression = 'Error' # 0으로 나눈 경우
            return 'Error'
        except:
            self.expression = 'Error' # 기타
            return 'Error'

    def _get_last_number(self):
        if not self.expression:
            return ''

        i = len(self.expression) - 1
        last_number = ''

        # 뒤에서부터 숫자 또는 소수점(.)을 수집
        while i >= 0 and (self.expression[i].isdigit() or self.expression[i] == '.'):
            last_number = self.expression[i] + last_number
            i -= 1

        # 음수 기호가 숫자 앞에 있다면 포함
        if i >= 0 and self.expression[i] == '-':
            if i == 0 or self.expression[i - 1] in '+-x÷':
                last_number = '-' + last_number

        return last_number

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())
