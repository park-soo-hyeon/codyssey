import zipfile
import itertools
import time
import zlib  # zlib 모듈을 추가로 import 합니다.

def unlock_zip():
    zip_path = 'emergency_storage_key.zip'
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    
    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    
    print(f'시작 시간: {start_time_str}')
    
    attempts = 0
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            target_file = zf.namelist()[0]
            
            for combo in itertools.product(characters, repeat=6):
                attempts += 1
                password = ''.join(combo)
                
                if attempts % 100000 == 0:
                    current_time = time.time()
                    elapsed = current_time - start_time
                    print(f'반복 횟수: {attempts}, 진행 시간: {elapsed:.2f}초, 시도 중인 암호: {password}')
                
                try:
                    zf.read(target_file, pwd=password.encode('utf-8'))
                    
                    final_time = time.time()
                    total_elapsed = final_time - start_time
                    
                    print(f'\n[성공] 비밀번호를 찾았습니다: {password}')
                    print(f'총 반복 횟수: {attempts}, 총 소요 시간: {total_elapsed:.2f}초')
                    
                    with open('password.txt', 'w') as f:
                        f.write(password)
                    
                    zf.extractall(pwd=password.encode('utf-8'))
                    print('압축 해제가 완료되었습니다.')
                    
                    return password
                    
                # 수정된 부분: zlib.error와 Exception을 추가하여 튕기는 현상 방지
                except (RuntimeError, zipfile.BadZipFile, zlib.error):
                    pass
                except Exception:
                    pass
                    
    except FileNotFoundError:
        print('에러: emergency_storage_key.zip 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'파일 처리 중 알 수 없는 예외가 발생했습니다: {e}')

if __name__ == '__main__':
    unlock_zip()