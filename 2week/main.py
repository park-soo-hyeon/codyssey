def main():
    file_name = 'Mars_Base_Inventory_List.csv'
    danger_file_name = 'Mars_Base_Inventory_danger.csv'
    binary_file_name = 'Mars_Base_Inventory_List.bin'

    inventory_list = []
    header = ''

    # 1. 파일 읽기 및 출력, 리스트로 변환 (수행과제 1, 2)
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            print('--- 전체 화물 목록 원본 ---')
            for index, line in enumerate(lines):
                clean_line = line.strip()
                print(clean_line)
                
                if index == 0:
                    header = clean_line
                else:
                    # 빈 줄이 있을 경우를 대비한 예외 처리
                    if clean_line: 
                        item_list = clean_line.split(',')
                        inventory_list.append(item_list)
                        
    except FileNotFoundError:
        print('입고 목록 파일(CSV)을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'파일을 읽는 중 에러가 발생했습니다: {e}')
        return

    # 2. 인화성(Flammability) 높은 순으로 정렬 (수행과제 3)
    # 마지막 열([-1])의 값을 실수(float)로 변환하여 내림차순(reverse=True) 정렬
    inventory_list.sort(key=lambda x: float(x[-1]), reverse=True)

    # 3. 인화성 지수 0.7 이상 추출 및 화면 출력 (수행과제 4)
    danger_list = []
    print('\n--- 인화성 지수 0.7 이상 위험 물질 목록 ---')
    for item in inventory_list:
        flammability = float(item[-1])
        if flammability >= 0.7:
            danger_list.append(item)
            print(','.join(item))

    # 4. 위험 물질을 새로운 CSV 파일로 저장 (수행과제 5)
    try:
        with open(danger_file_name, 'w', encoding='utf-8') as f:
            f.write(header + '\n')
            for item in danger_list:
                f.write(','.join(item) + '\n')
        print(f'\n[저장 완료] 위험 물질 목록 파일: {danger_file_name}')
    except Exception as e:
        print(f'위험 물질 파일 저장 중 에러가 발생했습니다: {e}')

    # 5. 보너스 과제: 정렬된 전체 목록을 이진 파일(bin)로 저장 및 읽기
    try:
        # 이진 파일로 쓰기 ('wb' 모드, utf-8로 인코딩)
        with open(binary_file_name, 'wb') as f:
            f.write((header + '\n').encode('utf-8'))
            for item in inventory_list:
                f.write((','.join(item) + '\n').encode('utf-8'))
        print(f'[저장 완료] 전체 목록 이진 파일: {binary_file_name}')
        
        # 저장된 이진 파일을 다시 읽어와서 화면에 출력 ('rb' 모드, 디코딩)
        print('\n--- 이진 파일(Binary)에서 다시 읽어들인 내용 ---')
        with open(binary_file_name, 'rb') as f:
            binary_data = f.read()
            print(binary_data.decode('utf-8').strip())
            
    except Exception as e:
        print(f'이진 파일을 처리하는 중 에러가 발생했습니다: {e}')


if __name__ == '__main__':
    main()