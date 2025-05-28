import os
import sounddevice as sd
import wave
from datetime import datetime


def create_record_directory():
    if not os.path.exists('./02_problem_05_07/records'):
        os.makedirs('./02_problem_05_07/records')


def get_timestamp():
    now = datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')


def record_audio(duration=5, samplerate=44100):
    print('🎙️ 녹음을 시작합니다. 말해주세요...')
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print('✅ 녹음이 완료되었습니다.')
    return audio_data


def save_wave_file(data, filename, samplerate=44100):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)               # 모노
        wf.setsampwidth(2)               # 16비트 → 2바이트
        wf.setframerate(samplerate)
        wf.writeframes(data.tobytes())


def main():
    create_record_directory()
    timestamp = get_timestamp()
    filename = f'./02_problem_05_07/records/{timestamp}.wav'

    try:
        audio_data = record_audio(duration=5)  # 5초간 녹음
        save_wave_file(audio_data, filename)
        print(f'📁 저장 완료: {filename}')
    except Exception as e:
        print(f'⚠️ 녹음 중 오류 발생: {e}')


# 📅 보너스 기능: 특정 날짜 범위의 파일 조회
def list_recordings_by_date(start_date, end_date):
    try:
        start = datetime.strptime(start_date, '%Y%m%d')
        end = datetime.strptime(end_date, '%Y%m%d')

        print(f'\n📂 [{start_date} ~ {end_date}] 녹음 파일 목록:')
        for file in os.listdir('records'):
            if file.endswith('.wav'):
                file_date = datetime.strptime(file.split('-')[0], '%Y%m%d')
                if start <= file_date <= end:
                    print('  -', file)
    except Exception as e:
        print(f'⚠️ 날짜 필터링 오류: {e}')


if __name__ == '__main__':
    main()

    # ▶ 보너스 테스트 예시
    # list_recordings_by_date('20240501', '20240514')  # 원하는 날짜 범위로 수정
