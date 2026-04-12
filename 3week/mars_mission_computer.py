import random
import datetime

class DummySensor:
    def __init__(self):
        # DummySensor의 멤버로 env_values라는 사전 객체를 추가
        self.env_values = {}

    def set_env(self):
        # random으로 주어진 범위 안의 값을 생성해서 env_values 항목에 채움
        self.env_values = {
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 4),
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2)
        }

    def get_env(self):
        # 보너스 과제: 파일에 log를 남기는 부분을 추가
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 문자열 내에서 홑따옴표(')를 사용해야 하므로 곁따옴표("")를 사용
        log_data = (
            f"{now}, "
            f"내부 온도: {self.env_values['mars_base_internal_temperature']}, "
            f"외부 온도: {self.env_values['mars_base_external_temperature']}, "
            f"내부 습도: {self.env_values['mars_base_internal_humidity']}, "
            f"외부 광량: {self.env_values['mars_base_external_illuminance']}, "
            f"내부 이산화탄소 농도: {self.env_values['mars_base_internal_co2']}, "
            f"내부 산소 농도: {self.env_values['mars_base_internal_oxygen']}\n"
        )
        
        with open('./3week/sensor_log.txt', 'a', encoding='utf-8') as file:
            file.write(log_data)
            
        # env_values를 return 함
        return self.env_values

# DummySensor 클래스를 ds라는 이름으로 인스턴스(Instance)로 만듦
ds = DummySensor()

# set_env()와 get_env()를 차례로 호출해서 값을 확인
ds.set_env()
current_env = ds.get_env()

print(current_env)