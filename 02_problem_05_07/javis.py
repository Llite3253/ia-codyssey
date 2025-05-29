import os                     # 파일 및 디렉토리 작업을 위한 표준 라이브러리
import sounddevice as sd      # 오디오 녹음을 위한 라이브러리
import wave                   # WAV 파일 저장을 위한 라이브러리
from datetime import datetime # 날짜 및 시간 처리를 위한 모듈

# records 디렉토리가 없으면 생성하는 함수
def create_record_directory():
    if not os.path.exists('records'): # 'records' 폴더가 없으면
        os.makedirs('records') # 폴더 생성

# 현재 시각을 'YYYYMMDD-HHMMSS' 형식의 문자열로 반환하는 함수
def get_timestamp():
    now = datetime.now() # 현재 시각 가져오기
    return now.strftime('%Y%m%d-%H%M%S') # 문자열로 변환하여 반환

# 마이크로부터 일정 시간 오디오를 녹음하는 함수
def record_audio(duration=5, samplerate=44100):
    print('\n🎙️ 녹음을 시작합니다. 말해주세요...')
    audio_data = sd.rec( # 오디오 녹음 시작
        int(duration * samplerate), # 녹음할 샘플 수 계산
        samplerate=samplerate, # 샘플링 주파수 설정
        channels=1, # 채널 수: 1 (모노)
        dtype='int16') # 샘플 형식: 16비트 정수
    sd.wait() # 녹음이 끝날 때까지 대기
    print('✅ 녹음이 완료되었습니다.')
    return audio_data # 녹음된 오디오 데이터 반환

# 녹음된 데이터를 WAV 파일로 저장하는 함수
def save_wave_file(data, filename, samplerate=44100):
    with wave.open(filename, 'w') as wf: # WAV 파일 쓰기 모드로 열기
        wf.setnchannels(1) # 모노 채널
        wf.setsampwidth(2) # 샘플 너비: 2바이트 = 16비트
        wf.setframerate(samplerate) # 샘플링 주파수 설정
        wf.writeframes(data.tobytes()) # 오디오 데이터를 바이트로 저장

# 전체 녹음 과정을 관리하는 함수
def start_recording():
    create_record_directory() # 디렉토리 생성 (없으면)
    timestamp = get_timestamp() # 타임스탬프 문자열 생성
    filename = f'records/{timestamp}.wav' # 저장할 파일 경로 구성

    try:
        audio_data = record_audio(duration=5) # 오디오 녹음 수행
        save_wave_file(audio_data, filename) # 녹음 파일 저장
        print(f'📁 저장 완료: {filename}')
    except Exception as e: # 오류 발생 시 메시지 출력
        print(f'⚠️ 녹음 중 오류 발생: {e}')

# 날짜별 녹음 파일을 필터링하여 보여주는 함수
def list_recordings_by_date():
    try:
        start_input = input('🗓 시작 날짜를 입력하세요 (예: 20240501): ') # 시작일 입력
        end_input = input('🗓 종료 날짜를 입력하세요 (예: 20240514): ') # 종료일 입력
        start = datetime.strptime(start_input, '%Y%m%d') # 문자열 → 날짜 변환
        end = datetime.strptime(end_input, '%Y%m%d')

        print(f'\n📂 [{start_input} ~ {end_input}] 녹음 파일 목록:')
        found = False
        for file in os.listdir('records'): # records 폴더 내 모든 파일 확인
            if file.endswith('.wav'): # WAV 파일만 필터링
                file_date = datetime.strptime(file.split('-')[0], '%Y%m%d') # 파일 이름에서 날짜 추출
                if start <= file_date <= end: # 날짜가 범위에 포함되면
                    print('  -', file) # 파일명 출력
                    found = True

        if not found:
            print('📭 해당 기간에 녹음된 파일이 없습니다.') # 결과 없음 메시지 출력
    except Exception as e:
        print(f'⚠️ 날짜 필터링 오류: {e}') # 오류 메시지 출력

# 프로그램 실행 시작점
def main():
    print('📢 자비스 작동 시작') # 시작 메시지 출력
    print('1: 🎙️ 녹음 시작') # 메뉴 안내
    print('2: 📂 녹음 파일 목록 보기')
    choice = input('👉 작업을 선택하세요 (1 또는 2): ') # 사용자 입력 받기

    if choice == '1':
        start_recording() # 녹음 시작
    elif choice == '2':
        list_recordings_by_date() # 녹음 목록 출력
    else:
        print('❌ 잘못된 선택입니다. 프로그램을 종료합니다.') # 잘못된 선택 안내

# 이 파일이 메인 프로그램으로 실행될 경우 main() 호출
if __name__ == '__main__':
    main()
