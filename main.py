# 로그 파일 경로로
log_file_path = "C:/codyssey/01/mission_computer_main.log"
error_log_file = "C:/codyssey/01/error_logs.txt"

try: # 예외 처리
    # 로그 파일 읽기기
    with open(log_file_path, 'r', encoding='utf-8') as f: # with 사용이유: close를 호출할 필요가 없음음
        l = f.readlines()

    l.reverse() # 역순

    print("\n--- 로그 파일 내용 ---\n")
    for line in l:
        print(line.strip()) # strip 사용 이유: 데이터를 읽고 출력할 때 줄 끝에 남아 있는 개행문자(\n)나 불필요한 공백 제거거

    # 리스트 컴프리헨션을 사용하여 로그 데이터에서 오류 메시지를 포함하는 줄만 필터링
    # 필터링은 '불안정한', '폭발' 로 설정
    error_logs = [line for line in l if "unstable" in line or "explosion" in line]

    if error_logs:
        with open(error_log_file, 'w', encoding='utf-8') as f:
            f.write("timestamp,event,message\n") # 파일이 없을 경우 빈 파일 생성성
            f.writelines(error_logs)

        # f-string 으로 f를 사용하여 문자열 안에서 변수를 바로 사용용
        print(f"\n문제가 되는 로그를 '{error_log_file}' 경로로 저장되었습니다.")

except FileNotFoundError: # 파일이 존재하지 않을 때 발생하는 오류
    print(f"error: 로그 파일 '{log_file_path}' 을(를) 찾을 수 없습니다.")
except Exception as e:
    print(f"예기치 않은 오류 발생: {e}")