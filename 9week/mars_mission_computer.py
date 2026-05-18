def caesar_cipher_decode(target_text):
    # [보너스 과제] 텍스트 사전 (Dictionary) 생성
    # 스토리 상 등장했던 단어나 화성 기지, 시스템과 관련된 흔한 영단어들로 구성
    dictionary = ['emergency', 'storage', 'password', 'open', 'door', 'system', 'admin', 'mars', 'base']
    
    decoded_results = {}
    is_stopped = False
    
    print('--- 카이사르 암호 해독 시작 ---')
    
    # 자리수(shift)를 알파벳 수(1~26)만큼 반복
    for shift in range(1, 27):
        decoded_text = ''
        
        # 문자열을 하나씩 확인하여 자리수만큼 밀어내기 (복호화)
        for char in target_text:
            if char.isalpha():
                # 소문자인 경우
                if char.islower():
                    decoded_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                # 대문자인 경우
                else:
                    decoded_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # 알파벳이 아닌 특수문자나 공백은 그대로 유지
                decoded_text += char
        
        # 결과를 사전에 저장하고 화면에 출력
        decoded_results[shift] = decoded_text
        print(f'[Shift {shift:2d}] {decoded_text}')
        
        # [보너스 과제] 사전에 있는 단어와 일치하는 키워드가 있는지 검사
        for word in dictionary:
            if word in decoded_text.lower():
                print(f'\n>>> 💡 [보너스 과제 성공] 사전에 등록된 의미 있는 단어("{word}")가 발견되었습니다!')
                print('>>> 불필요한 연산을 막기 위해 탐색 반복을 즉시 중단합니다.')
                is_stopped = True
                break
        
        # 단어가 발견되었으면 바깥쪽 반복문도 중단
        if is_stopped:
            break

    print('-' * 50)
    
    # 눈으로 식별 후 번호를 입력받아 파일로 저장하는 로직
    while True:
        try:
            user_input = input('해석이 완료된 올바른 문장의 번호(Shift)를 입력하세요: ')
            selected_shift = int(user_input)
            
            # 입력받은 번호가 방금까지 탐색한 결과 목록에 있는지 확인
            if selected_shift in decoded_results:
                final_text = decoded_results[selected_shift]
                print(f'\n선택된 올바른 문장: {final_text}')
                
                # 파일 저장 (예외 처리 포함)
                try:
                    with open('result.txt', 'w', encoding='utf-8') as f:
                        f.write(final_text)
                    print('✅ result.txt 파일에 최종 암호를 성공적으로 저장했습니다! 문이 열립니다!')
                except Exception as e:
                    print(f'❌ 파일 저장 중 오류가 발생했습니다: {e}')
                
                # 정상적으로 끝났으므로 무한 루프 탈출
                break
            else:
                print('목록에 출력된 올바른 번호를 입력해 주세요.')
                
        except ValueError:
            print('❌ 올바른 숫자를 입력해 주세요.')

def main():
    # 파일을 읽어오는 부분 (모든 파일 다루는 부분 예외 처리 적용)
    try:
        with open('password.txt', 'r', encoding='utf-8') as f:
            target_text = f.read().strip()
            
        if not target_text:
            print('password.txt 파일이 비어있습니다. 암호가 맞는지 확인해 주세요.')
            return
            
        # 완성된 함수 호출
        caesar_cipher_decode(target_text)
        
    except FileNotFoundError:
        print('❌ password.txt 파일을 찾을 수 없습니다. 코드를 실행하는 폴더에 파일이 있는지 확인해 주세요.')
    except Exception as e:
        print(f'❌ 파일을 읽는 중 알 수 없는 오류가 발생했습니다: {e}')

if __name__ == '__main__':
    main()