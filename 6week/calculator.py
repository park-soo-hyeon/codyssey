import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # 계산을 위한 상태 변수 초기화
        self.current_input = '0'
        self.previous_input = ''
        self.operator = ''
        self.is_new_input = True
        
        self.init_ui()

    def init_ui(self):
        # 윈도우 기본 설정
        self.setWindowTitle('Calculator')
        self.setFixedSize(320, 500)
        self.setStyleSheet('background-color: black;')

        main_layout = QVBoxLayout()
        
        # 디스플레이 영역 설정 (우측 정렬)
        self.display = QLabel('0')
        self.display.setStyleSheet('color: white; font-size: 50px; padding: 10px;')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        main_layout.addWidget(self.display)

        # 버튼 그리드 레이아웃 설정
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        # 버튼 텍스트와 그리드 위치(row, col, rowspan, colspan) 매핑
        buttons = {
            'AC': (0, 0, 1, 1), '+/-': (0, 1, 1, 1), '%': (0, 2, 1, 1), '÷': (0, 3, 1, 1),
            '7': (1, 0, 1, 1), '8': (1, 1, 1, 1), '9': (1, 2, 1, 1), '×': (1, 3, 1, 1),
            '4': (2, 0, 1, 1), '5': (2, 1, 1, 1), '6': (2, 2, 1, 1), '-': (2, 3, 1, 1),
            '1': (3, 0, 1, 1), '2': (3, 1, 1, 1), '3': (3, 2, 1, 1), '+': (3, 3, 1, 1),
            '0': (4, 0, 1, 2), '.': (4, 2, 1, 1), '=': (4, 3, 1, 1)
        }

        # 버튼 생성 및 스타일 적용
        for btn_text, pos in buttons.items():
            button = QPushButton(btn_text)
            
            # 아이폰 계산기와 유사한 스타일링 (색상 및 모양)
            if btn_text in ['÷', '×', '-', '+', '=']:
                button.setStyleSheet('background-color: #FF9F0A; color: white; font-size: 24px; border-radius: 30px;')
            elif btn_text in ['AC', '+/-', '%']:
                button.setStyleSheet('background-color: #A5A5A5; color: black; font-size: 20px; border-radius: 30px;')
            else:
                button.setStyleSheet('background-color: #333333; color: white; font-size: 28px; border-radius: 30px;')
            
            # 버튼 크기 설정 (0 버튼은 2칸 차지하므로 가로를 길게)
            if btn_text == '0':
                button.setFixedSize(140, 65)
            else:
                button.setFixedSize(65, 65)
                
            # 클릭 이벤트 연결
            button.clicked.connect(self.button_clicked)
            grid_layout.addWidget(button, pos[0], pos[1], pos[2], pos[3])

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def button_clicked(self):
        # 어떤 버튼이 눌렸는지 텍스트 가져오기
        sender = self.sender().text()

        # 숫자 버튼 처리
        if sender in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if self.is_new_input:
                self.current_input = sender
                self.is_new_input = False
            else:
                if self.current_input == '0':
                    self.current_input = sender
                else:
                    self.current_input += sender
            self.update_display(self.current_input)

        # 초기화 (AC)
        elif sender == 'AC':
            self.current_input = '0'
            self.previous_input = ''
            self.operator = ''
            self.is_new_input = True
            self.update_display(self.current_input)

        # 부호 반전 (+/-)
        elif sender == '+/-':
            if self.current_input != '0':
                if self.current_input.startswith('-'):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.update_display(self.current_input)

        # 백분율 (%)
        elif sender == '%':
            try:
                self.current_input = str(float(self.current_input) / 100)
                self.update_display(self.current_input)
                self.is_new_input = True
            except ValueError:
                pass

        # 소수점 (.)
        elif sender == '.':
            if '.' not in self.current_input:
                self.current_input += '.'
                self.update_display(self.current_input)

        # 4칙 연산자 (+, -, ×, ÷)
        elif sender in ['+', '-', '×', '÷']:
            if self.operator and not self.is_new_input:
                self.calculate_result()
            self.previous_input = self.current_input
            self.operator = sender
            self.is_new_input = True

        # 계산 실행 (=)
        elif sender == '=':
            if self.operator:
                self.calculate_result()
                self.operator = ''
                self.is_new_input = True

    def calculate_result(self):
        # 보너스 과제: 4칙 연산 처리 로직
        try:
            num1 = float(self.previous_input)
            num2 = float(self.current_input)
            result = 0

            if self.operator == '+':
                result = num1 + num2
            elif self.operator == '-':
                result = num1 - num2
            elif self.operator == '×':
                result = num1 * num2
            elif self.operator == '÷':
                if num2 == 0:
                    self.current_input = 'Error'
                    self.update_display(self.current_input)
                    return
                result = num1 / num2

            # 정수일 경우 소수점(.0) 제거
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(result)
                
            self.update_display(self.current_input)
            
        except ValueError:
            self.current_input = 'Error'
            self.update_display(self.current_input)

    def update_display(self, text):
        # 디스플레이 업데이트 (에러가 아닐 경우 천 단위 콤마 추가)
        if text == 'Error':
            self.display.setText(text)
            return
            
        try:
            if '.' in text:
                parts = text.split('.')
                formatted_text = f'{int(parts[0]):,}.{parts[1]}'
            else:
                formatted_text = f'{int(text):,}'
            self.display.setText(formatted_text)
        except ValueError:
            self.display.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())