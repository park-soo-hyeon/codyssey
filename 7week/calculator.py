import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # 계산기 핵심 상태 변수
        self.current_input = '0'
        self.stored_value = ''
        self.operator = ''
        self.new_input_flag = True
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(320, 500)
        self.setStyleSheet('background-color: black;')

        main_layout = QVBoxLayout()
        
        # 디스플레이 영역
        self.display = QLabel('0')
        self.display.setStyleSheet('color: white; font-size: 50px; padding: 10px;')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        main_layout.addWidget(self.display)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        buttons = {
            'AC': (0, 0, 1, 1), '+/-': (0, 1, 1, 1), '%': (0, 2, 1, 1), '÷': (0, 3, 1, 1),
            '7': (1, 0, 1, 1), '8': (1, 1, 1, 1), '9': (1, 2, 1, 1), '×': (1, 3, 1, 1),
            '4': (2, 0, 1, 1), '5': (2, 1, 1, 1), '6': (2, 2, 1, 1), '-': (2, 3, 1, 1),
            '1': (3, 0, 1, 1), '2': (3, 1, 1, 1), '3': (3, 2, 1, 1), '+': (3, 3, 1, 1),
            '0': (4, 0, 1, 2), '.': (4, 2, 1, 1), '=': (4, 3, 1, 1)
        }

        for btn_text, pos in buttons.items():
            button = QPushButton(btn_text)
            
            if btn_text in ['÷', '×', '-', '+', '=']:
                button.setStyleSheet('background-color: #FF9F0A; color: white; font-size: 24px; border-radius: 30px;')
            elif btn_text in ['AC', '+/-', '%']:
                button.setStyleSheet('background-color: #A5A5A5; color: black; font-size: 20px; border-radius: 30px;')
            else:
                button.setStyleSheet('background-color: #333333; color: white; font-size: 28px; border-radius: 30px;')
            
            if btn_text == '0':
                button.setFixedSize(140, 65)
            else:
                button.setFixedSize(65, 65)
                
            button.clicked.connect(self.button_clicked)
            grid_layout.addWidget(button, pos[0], pos[1], pos[2], pos[3])

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    # --- 버튼 이벤트 분배 ---
    def button_clicked(self):
        sender = self.sender().text()

        if sender in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.input_number(sender)
        elif sender == '.':
            self.input_decimal()
        elif sender == 'AC':
            self.reset()
        elif sender == '+/-':
            self.negative_positive()
        elif sender == '%':
            self.percent()
        elif sender in ['+', '-', '×', '÷']:
            self.set_operator(sender)
        elif sender == '=':
            self.equal()

    # --- 계산기 핵심 기능(메소드) ---
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError('0으로 나눌 수 없습니다.')
        return a / b

    def reset(self):
        self.current_input = '0'
        self.stored_value = ''
        self.operator = ''
        self.new_input_flag = True
        self.update_display(self.current_input)

    def negative_positive(self):
        if self.current_input != '0' and self.current_input != 'Error':
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display(self.current_input)

    def percent(self):
        try:
            val = float(self.current_input) / 100
            val = round(val, 6) # 보너스: 6자리 반올림 적용
            if val.is_integer():
                self.current_input = str(int(val))
            else:
                self.current_input = str(val)
            self.update_display(self.current_input)
            self.new_input_flag = True
        except ValueError:
            pass

    def input_number(self, num_str):
        if self.new_input_flag:
            self.current_input = num_str
            self.new_input_flag = False
        else:
            if self.current_input == '0':
                self.current_input = num_str
            else:
                self.current_input += num_str
        self.update_display(self.current_input)

    def input_decimal(self):
        # 소수점 중복 입력 방지
        if '.' not in self.current_input:
            self.current_input += '.'
            self.update_display(self.current_input)
            self.new_input_flag = False

    def set_operator(self, op):
        if self.operator and not self.new_input_flag:
            self.equal()
        self.stored_value = self.current_input
        self.operator = op
        self.new_input_flag = True

    def equal(self):
        if not self.operator or not self.stored_value:
            return

        try:
            a = float(self.stored_value)
            b = float(self.current_input)
            result = 0

            if self.operator == '+':
                result = self.add(a, b)
            elif self.operator == '-':
                result = self.subtract(a, b)
            elif self.operator == '×':
                result = self.multiply(a, b)
            elif self.operator == '÷':
                result = self.divide(a, b)

            # 보너스 과제: 소수점 6자리 이하 반올림
            result = round(result, 6)

            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(result)

            self.operator = ''
            self.new_input_flag = True
            self.update_display(self.current_input)

        except ZeroDivisionError:
            self.show_error('Error: Div by 0')
        except OverflowError:
            self.show_error('Error: Overflow')
        except Exception:
            self.show_error('Error')

    # --- UI 업데이트 및 예외 처리 헬퍼 ---
    def update_display(self, text):
        if text.startswith('Error'):
            return

        try:
            # 천 단위 콤마 추가
            if '.' in text:
                parts = text.split('.')
                formatted_text = f'{int(parts[0]):,}.{parts[1]}'
            else:
                formatted_text = f'{int(text):,}'
        except ValueError:
            formatted_text = text

        # 보너스 과제: 출력 길이(문자 수)에 따른 폰트 크기 동적 조절
        length = len(formatted_text)
        if length <= 9:
            font_size = 50
        else:
            # 글자가 길어질수록 폰트를 줄임 (최소 20px)
            font_size = max(20, 50 - (length - 9) * 3)

        self.display.setStyleSheet(f'color: white; font-size: {font_size}px; padding: 10px;')
        self.display.setText(formatted_text)

    def show_error(self, message):
        self.current_input = 'Error'
        self.display.setStyleSheet('color: #FF3B30; font-size: 35px; padding: 10px;')
        self.display.setText(message)
        self.new_input_flag = True
        self.operator = ''
        self.stored_value = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())