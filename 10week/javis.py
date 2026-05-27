import os
import wave
import datetime
import array
import threading
import sys


RECORDS_DIR = RECORDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'records')
SAMPLE_RATE = 44100
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit audio
CHUNK_SIZE = 1024


def ensure_records_dir():
    """records 폴더가 없으면 생성한다."""
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)


def get_filename():
    """현재 날짜와 시간을 기반으로 파일명을 생성한다. (년월일-시간분초)"""
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S') + '.wav'


def record_audio():
    """마이크로부터 음성을 녹음하고 records 폴더에 저장한다."""
    try:
        import pyaudio
    except ImportError:
        print('[오류] pyaudio 라이브러리가 설치되어 있지 않습니다.')
        print('설치 명령어: pip install pyaudio')
        return

    ensure_records_dir()
    filename = get_filename()
    filepath = os.path.join(RECORDS_DIR, filename)

    audio = pyaudio.PyAudio()

    # 마이크 장치 확인
    device_count = audio.get_device_count()
    input_device = None
    for i in range(device_count):
        info = audio.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            input_device = i
            break

    if input_device is None:
        print('[오류] 사용 가능한 마이크를 찾을 수 없습니다.')
        audio.terminate()
        return

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        input_device_index=input_device,
        frames_per_buffer=CHUNK_SIZE
    )

    print(f'녹음을 시작합니다. 저장 파일: {filepath}')
    print('녹음을 중지하려면 Enter 키를 누르세요...')

    frames = []
    is_recording = [True]

    def stop_on_enter():
        input()
        is_recording[0] = False

    stop_thread = threading.Thread(target=stop_on_enter, daemon=True)
    stop_thread.start()

    while is_recording[0]:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # WAV 파일로 저장
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))

    print(f'녹음이 완료되었습니다. 저장 위치: {filepath}')


def show_records_by_date_range(start_date_str, end_date_str):
    """특정 범위의 날짜에 해당하는 녹음 파일을 보여준다. (보너스 과제)

    Args:
        start_date_str: 시작 날짜 문자열 (YYYYMMDD 형식)
        end_date_str: 종료 날짜 문자열 (YYYYMMDD 형식)
    """
    ensure_records_dir()

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d').date()
    except ValueError:
        print('[오류] 날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 입력하세요.')
        return

    if start_date > end_date:
        print('[오류] 시작 날짜가 종료 날짜보다 늦을 수 없습니다.')
        return

    matched_files = []

    for filename in os.listdir(RECORDS_DIR):
        if not filename.endswith('.wav'):
            continue
        name_part = filename.replace('.wav', '')
        try:
            file_date_str = name_part.split('-')[0]
            file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d').date()
            if start_date <= file_date <= end_date:
                matched_files.append(filename)
        except (ValueError, IndexError):
            continue

    matched_files.sort()

    if matched_files:
        print(f'\n[{start_date_str} ~ {end_date_str}] 범위의 녹음 파일 목록:')
        for i, filename in enumerate(matched_files, start=1):
            filepath = os.path.join(RECORDS_DIR, filename)
            size_kb = os.path.getsize(filepath) / 1024
            print(f'  {i}. {filename}  ({size_kb:.1f} KB)')
        print(f'\n총 {len(matched_files)}개의 파일이 있습니다.')
    else:
        print(f'[{start_date_str} ~ {end_date_str}] 범위에 해당하는 녹음 파일이 없습니다.')


def show_menu():
    """메인 메뉴를 출력한다."""
    print('\n===== JAVIS 음성 녹음 시스템 =====')
    print('1. 음성 녹음 시작')
    print('2. 날짜 범위로 녹음 파일 조회 (보너스)')
    print('3. 종료')
    print('==================================')


def run():
    """메인 실행 함수."""
    while True:
        show_menu()
        choice = input('메뉴를 선택하세요 (1~3): ').strip()

        if choice == '1':
            record_audio()
        elif choice == '2':
            start = input('시작 날짜를 입력하세요 (YYYYMMDD): ').strip()
            end = input('종료 날짜를 입력하세요 (YYYYMMDD): ').strip()
            show_records_by_date_range(start, end)
        elif choice == '3':
            print('프로그램을 종료합니다.')
            sys.exit(0)
        else:
            print('[오류] 올바른 메뉴 번호를 입력하세요.')


if __name__ == '__main__':
    run()