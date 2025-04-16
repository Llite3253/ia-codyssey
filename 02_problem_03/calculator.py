import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.engine = CalculatorEngine() # 계산 로직 클래스 생성
        self.init_ui() # UI 호출

    def init_ui(self):
        self.result_display = QLineEdit('0', readOnly=True) # 초기값 0
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setFont(QFont('맑은 고딕'))
        self.result_display.setStyleSheet('font-size: 30px; color: white; border: none; padding-right: 5px;')
        self.result_display.setFixedHeight(50)

        main_layout = QVBoxLayout() # 전체 수직 레이아웃 생성
        button_layout = QGridLayout() # 버튼 배치를 위한 그리드 레이아웃 생성
        # 버튼 텍스트 배열
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 버튼 생성 및 레이아웃에 배치
        for row_idx, row in enumerate(buttons): # 행
            for col_idx, btn_text in enumerate(row): # 열
                button = QPushButton(btn_text) # 버튼 생성
                button.setFont(QFont('맑은 고딕')) # 폰트 설정

                if btn_text == '0':
                    button.setFixedSize(145, 70) # 0 버튼은 2칸 차지로 크기 설정
                else:
                    button.setFixedSize(70, 70) # 일반 버튼

                self.set_button_style(button, btn_text) # 버튼 색상 스타일 설정 함수
                button.clicked.connect(lambda _, text=btn_text: self.on_button_click(text)) # 버튼 클릭 이벤트 연결

                if btn_text == '0':
                    button_layout.addWidget(button, row_idx + 1, 0, 1, 2) # 0 버튼을 2칸 차지로 하기 위해 레이아웃 설정
                else:
                    offset = 1 if row_idx == 4 and col_idx >= 1 else 0 # 마지막 줄 보정
                    button_layout.addWidget(button, row_idx + 1, col_idx + offset)

        main_layout.addWidget(self.result_display) # 결과창 추가
        main_layout.addLayout(button_layout) # 버튼 레이아웃 추가
        self.setLayout(main_layout) # 최종 레이아웃 설정
        self.setWindowTitle('Calculator') # 창 제목 설정
        self.setFixedSize(320, 480) # 고정 크기 설정
        self.setStyleSheet('background-color: #000000') # 배경색 설정

    # 버튼 클릭 시 처리 함수
    def on_button_click(self, text):
        result = self.engine.input(text) # 계산 로직에 입력 전달 및 결과 받기
        self.result_display.setText(str(result)) # 결과창에 출력
        if text == '.':
            pass

    # 버튼 스타일 설정
    def set_button_style(self, button, text):
        style = "font-size: 24px; border-radius: 35px;"
        if text in ['÷', 'x', '-', '+', '=']:
            style += "background-color: #F6A000; color: white;"
        elif text in ['AC', '+/-', '%']:
            style += "background-color: #AFAFAF; color: black;"
        else:
            style += "background-color: #393939; color: #CDCDCD;"
        button.setStyleSheet(style)

# 계산 로직 클래스
class CalculatorEngine:
    def __init__(self):
        self.expression = '' # 현재 수식 문자열
        self.waiting_for_new_input = False # 다음 숫자 입력 대기 여부

    def input(self, text):
        if text == 'AC':
            self.expression = ''
            self.waiting_for_new_input = False
            return '0'
        elif text == '.':
            return self.expression
        elif text in ['+', '-', 'x', '÷']: # 연산자 입력
            if self.expression and self.expression[-1] in '+-x÷':
                self.expression = self.expression[:-1] + text # 연산자 중복 방지
            else:
                self.expression += text
            self.waiting_for_new_input = False
            return self.expression
        elif text == '=': # 계산 실행
            result = self.calculate()
            self.expression = str(result)
            self.waiting_for_new_input = True
            return str(result)
        else: # 숫자 입력
            if self.expression == '0':
                self.expression = text
            elif self.waiting_for_new_input:
                self.expression = text
                self.waiting_for_new_input = False
            else:
                self.expression += text
            return self.expression

    def calculate(self):
        try:
            expr = self.expression.replace('x', '*').replace('÷', '/')
            result = eval(expr)
            return int(result) if isinstance(result, float) and result.is_integer() else result
        except:
            return 'Error'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())