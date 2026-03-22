# main.py

# 1. 환경설정 확인용 테스트 출력
print('Hello Mars')
print('--------------------------------------------------') 

# 2. 로그 파일 읽기 및 예외 처리
def main():
    file_name = 'mission_computer_main.log'
    # 문제 되는 부분만 따로 저장할 새 파일 이름
    error_file_name = 'error.txt'

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # 보너스 문제 1: 출력 결과를 시간의 역순으로 정렬해서 출력
            lines.reverse()
            error_lines = []
            
            for line in lines:
                print(line.strip())
                
                # 보너스 문제 2: 출력 결과 중 문제가 되는 부분만 따로 파일로 저장
                if 'unstable' in line or 'explosion' in line:
                    error_lines.append(line)
        
        if error_lines: 
            with open(error_file_name, 'w', encoding='utf-8') as error_file:
                for error_line in error_lines:
                    error_file.write(error_line)
        
    except FileNotFoundError:
        print('로그 파일을 찾을 수 없습니다. 파일 이름을 확인해 주세요.')
    except Exception as e:
        print(f'알 수 없는 에러가 발생했습니다: {e}')

if __name__ == '__main__':
    main()