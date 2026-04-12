import os
import json
import platform

try:
    import psutil
except ImportError:
    print('오류: psutil 라이브러리가 설치되어 있지 않습니다.')
    print('터미널에서 "pip install psutil"을 실행하여 설치해 주세요.')
    exit()

class MissionComputer:
    def __init__(self):
        # 보너스 과제: 출력 항목 세팅을 위한 설정 파일 로드
        self.settings = self._load_settings()

    def _load_settings(self):
        """setting.txt 파일을 읽어서 설정값을 가져옵니다. 파일이 없으면 기본값으로 생성합니다."""
        setting_file = './5week/setting.txt'
        
        # 기본 출력 설정 (True면 출력, False면 출력 안 함)
        default_settings = {
            'show_os': 'True',
            'show_os_version': 'True',
            'show_cpu_type': 'True',
            'show_cpu_core': 'True',
            'show_memory_size': 'True',
            'show_cpu_usage': 'True',
            'show_memory_usage': 'True'
        }
        
        # 설정 파일이 없을 경우 기본값으로 생성
        if not os.path.exists(setting_file):
            try:
                with open(setting_file, 'w', encoding='utf-8') as file:
                    for key, value in default_settings.items():
                        file.write(f'{key}={value}\n')
            except Exception as e:
                print(f'설정 파일 생성 중 예외 발생: {e}')
            return {k: True for k in default_settings} # 기본적으로 모두 True 반환
        
        # 설정 파일이 존재할 경우 읽어오기
        loaded_settings = {}
        try:
            with open(setting_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=')
                        # 'True' 문자열이면 참, 그 외엔 거짓으로 처리
                        loaded_settings[key.strip()] = (value.strip() == 'True')
        except Exception as e:
            print(f'설정 파일 읽기 중 예외 발생: {e}')
            return {k: True for k in default_settings}
            
        return loaded_settings

    def get_mission_computer_info(self):
        """필요한 미션 컴퓨터의 시스템 정보를 가져오고 JSON으로 출력합니다."""
        sys_info = {}
        
        try:
            # setting.txt의 설정값에 따라 항목 추가
            if self.settings.get('show_os', True):
                sys_info['os'] = platform.system()
                
            if self.settings.get('show_os_version', True):
                sys_info['os_version'] = platform.version()
                
            if self.settings.get('show_cpu_type', True):
                sys_info['cpu_type'] = platform.processor()
                
            if self.settings.get('show_cpu_core', True):
                # 물리 코어 수를 가져오며, 실패할 경우 논리 코어 수 반환
                sys_info['cpu_core'] = psutil.cpu_count(logical=False) or psutil.cpu_count()
                
            if self.settings.get('show_memory_size', True):
                # 바이트 단위의 메모리를 GB 단위로 변환하여 소수점 둘째 자리까지 표시
                mem_gb = psutil.virtual_memory().total / (1024 ** 3)
                sys_info['memory_size'] = f'{mem_gb:.2f} GB'
                
        except Exception as e:
            # 요구사항: 시스템 정보를 가져오는 부분은 예외처리가 되어 있어야 한다.
            sys_info['error'] = f'시스템 정보 수집 실패: {e}'

        # JSON 형식으로 출력
        print('--- [시스템 정보] ---')
        print(json.dumps(sys_info, indent=4, ensure_ascii=False))
        return sys_info

    def get_mission_computer_load(self):
        """미션 컴퓨터의 실시간 부하(CPU, 메모리) 정보를 가져오고 JSON으로 출력합니다."""
        sys_load = {}
        
        try:
            if self.settings.get('show_cpu_usage', True):
                # CPU 사용량을 % 단위로 1초간 측정하여 가져옴
                sys_load['cpu_usage'] = f'{psutil.cpu_percent(interval=1)}%'
                
            if self.settings.get('show_memory_usage', True):
                # 메모리 사용량을 % 단위로 가져옴
                sys_load['memory_usage'] = f'{psutil.virtual_memory().percent}%'
                
        except Exception as e:
            sys_load['error'] = f'시스템 부하 수집 실패: {e}'

        # JSON 형식으로 출력
        print('\n--- [시스템 실시간 부하 정보] ---')
        print(json.dumps(sys_load, indent=4, ensure_ascii=False))
        return sys_load

# MissionComputer 클래스를 runComputer 라는 이름으로 인스턴스화
runComputer = MissionComputer()

if __name__ == '__main__':
    # runComputer 인스턴스의 메소드를 호출해서 시스템 정보 출력
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()