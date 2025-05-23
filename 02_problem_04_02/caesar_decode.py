def caesar_cipher_decode(target_text, dictionary):
    for shift in range(1, 26):  # 1~25 shift
        decoded = ''

        for ch in target_text:
            if 'a' <= ch <= 'z':
                decoded += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
            elif 'A' <= ch <= 'Z':
                decoded += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
            else:
                decoded += ch

        print(f'[Shift {shift:2}] {decoded}')

        for word in dictionary:
            if word.lower() in decoded.lower():
                print(f'\n키워드 "{word}" 발견! Shift {shift}가 정답입니다.')
                try:
                    with open('result.txt', 'w') as out:
                        out.write(decoded)
                    print('result.txt에 자동 저장하고 프로그램을 종료합니다.')
                except:
                    print('result.txt 저장 실패.')
                return True  # 종료 조건

    return False  # 키워드 발견 못함


def main():
    try:
        with open('password.txt', 'r') as f:
            encrypted = f.read().strip()
    except FileNotFoundError:
        print('password.txt 파일이 없습니다.')
        return

    keyword_dict = ['emergency', 'oxygen', 'mars', 'unlock', 'open', 'storage']

    print('password.txt의 카이사르 해독을 시작합니다...\n')
    found = caesar_cipher_decode(encrypted, keyword_dict)

    if not found:
        print('\n키워드가 자동으로 발견되지 않았습니다.')
        print('눈으로 확인 후 Shift 번호를 입력해주세요.')
        try:
            index = int(input('정답으로 추정되는 shift 번호 (1~25): '))
            if 1 <= index <= 25:
                decoded = ''
                for ch in encrypted:
                    if 'a' <= ch <= 'z':
                        decoded += chr((ord(ch) - ord('a') - index) % 26 + ord('a'))
                    elif 'A' <= ch <= 'Z':
                        decoded += chr((ord(ch) - ord('A') - index) % 26 + ord('A'))
                    else:
                        decoded += ch
                with open('result.txt', 'w') as out:
                    out.write(decoded)
                print('수동으로 result.txt에 저장 완료.')
            else:
                print('범위를 벗어난 숫자입니다.')
        except:
            print('입력 오류가 발생했습니다.')


if __name__ == '__main__':
    main()
