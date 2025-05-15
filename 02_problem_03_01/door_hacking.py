import time
import zipfile
from multiprocessing import Process, Value, Lock

found = Value('b', False) # 비밀번호를 찾았는지 여부를 공유하는 변수
lock = Lock() # 

def try_passwords(start_chars, charset, zip_path, found, lock, start_time):
    try:
        zf = zipfile.ZipFile(zip_path) # zip 파일 열기
    except:
        print('ZIP 파일 열기 실패') # 파일 열기에 실패한 경우
        return

    count = 0 # 시도 횟수 카운트 초기화
    for a in start_chars: # 각 프로세스가 맡은 시작 문자 반복
        for b in charset:
            for c in charset:
                for d in charset:
                    for e in charset:
                        for f in charset:
                            if found.value: # 다른 프로세스에서 이미 찾았는지 확인
                                return
                            pwd = a + b + c + d + e + f
                            count += 1
                            try:
                                zf.extractall(pwd=bytes(pwd, 'utf-8')) # 비밀번호로 압축 해제 시도
                                with lock:
                                    if not found.value: # 아직 비밀번호가 발견되지 않았다면
                                        found.value = True # 발견 표시
                                        print(f'\n 비밀번호 발견: {pwd}')
                                        print(f'시도 횟수: {count}')
                                        print(f'경과 시간: {time.time() - start_time:.2f}초')
                                        with open('password.txt', 'w') as f:
                                            f.write(pwd)
                                return
                            except:
                                if count % 10000 == 0: # 1만 번 시도마다 진행 상황 출력
                                    elapsed = time.time() - start_time
                                    print(f'[{a}] {count}회 시도 중... ({elapsed:.1f}초)')

def unlock_zip():
    zip_path = 'emergency_storage_key.zip'
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
    process_count = 12  # 사용하려는 프로세스 수

    split = len(charset) // process_count # 문자 집합을 프로세스 수만큼 균등 분할
    processes = [] # 생성한 프로세스들을 저장
    start_time = time.time() # 시작 시간 기록

    for i in range(process_count): # 각 프로세스에 문자 구간을 할당
        start_chars = charset[i * split: (i + 1) * split] # 할당된 시작 문자들
        p = Process(target=try_passwords, args=(start_chars, charset, zip_path, found, lock, start_time))
        p.start() # 프로세스 시작
        processes.append(p) # 리스트에 추가

    for p in processes: # 모든 프로세스가 종료될 때까지 대기
        p.join()

    if not found.value:
        print('비밀번호를 찾지 못했습니다.')

if __name__ == '__main__':
    unlock_zip()
