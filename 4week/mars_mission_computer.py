import time
import json
import random
import threading

class DummySensor:
    def __init__(self):
        self.env_values = {}

    def set_env(self):
        self.env_values = {
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 4),
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2)
        }

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        # 환경 값을 저장할 사전(Dict) 객체
        self.env_values = {}
        # 문제 3(이전 과제)에서 제작한 DummySensor 인스턴스화
        self.ds = DummySensor()
        
        # 시스템 동작 상태 제어용 변수
        self.is_running = True
        
        # 보너스 과제(5분 평균)를 위해 누적 데이터를 저장할 리스트
        self.history = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': []
        }

    def _wait_for_stop_key(self):
        # 특정 키(Enter) 입력을 감지하여 시스템을 멈추는 백그라운드 스레드용 메서드
        input('시스템을 종료하려면 Enter 키를 누르세요...\n')
        self.is_running = False

    def get_sensor_data(self):
        # 특정 키 입력을 비동기적으로 받기 위해 스레드 시작
        stop_thread = threading.Thread(target=self._wait_for_stop_key)
        stop_thread.daemon = True
        stop_thread.start()

        iteration_count = 0

        while self.is_running:
            # 센서 값을 생성하고 가져와서 env_values에 담기
            self.ds.set_env()
            self.env_values = self.ds.get_env()

            # 환경 정보의 값을 json 형태로 화면에 출력
            print(json.dumps(self.env_values, indent=4))

            # 보너스 과제: 5분 평균값을 위해 현재 값 누적
            for key, value in self.env_values.items():
                self.history[key].append(value)

            iteration_count += 1

            # 5분에 한 번씩(5초 x 60회 = 300초) 5분 평균값 출력
            if iteration_count >= 60:
                print('\n--- [5분 평균 환경값] ---')
                avg_values = {}
                for key, values in self.history.items():
                    avg = sum(values) / len(values)
                    avg_values[key] = round(avg, 4)
                
                print(json.dumps(avg_values, indent=4))
                print('-------------------------\n')

                # 다음 5분 측정을 위해 기록 초기화
                for key in self.history:
                    self.history[key].clear()
                iteration_count = 0

            # 5초 대기 (종료 신호를 빠르게 감지하기 위해 0.1초씩 50번 대기)
            for _ in range(50):
                if not self.is_running:
                    break
                time.sleep(0.1)

        # 시스템 종료 시 요구된 문구 출력 (원문 오타 그대로 반영)
        print('Sytem stoped…')

# MissionComputer 클래스를 RunComputer 라는 이름으로 인스턴스화
RunComputer = MissionComputer()

# 지속적으로 환경에 대한 값을 출력
if __name__ == '__main__':
    RunComputer.get_sensor_data()
