def read_csv_print(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print(f'파일 {file_path}을 찾을 수 없습니다.')
    except Exception as e:
        print(f'데이터 변환 중 오류가 발생했습니다: {e}')

def read_csv_file(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            header = f.readline().strip().split(',')
            for line in f:
                values = line.strip().split(',')
                if len(values) == len(header):
                    data.append(values)
    except FileNotFoundError:
        print(f'파일 {file_path}을 찾을 수 없습니다.')
    except Exception as e:
        print(f'데이터 변환 중 오류가 발생했습니다: {e}')
    return data, header

def sort_by_flammability(file_data):
    return sorted(file_data, key=lambda x: float(x[4]), reverse=True)

def filter_high_flammability(inventory_high_flammability_data):
    return [row for row in inventory_high_flammability_data if float(row[4]) >= 0.7]

def write_csv_file(file_path, data, header):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(','.join(header) + '\n')
            for i in data:
                f.write(','.join(i) + '\n')
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')

def write_binary_file(file_path, data, header):
    try:
        with open(file_path, 'wb') as f:
            f.write(','.join(header).encode('utf-8') + b'\n')
            for i in data:
                f.write(','.join(i).encode('utf-8') + b'\n')
    except Exception as e:
        print(f'이진 파일 저장 중 오류 발생: {e}')

def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            for line in f:
                print(line.decode('utf-8').strip())
    except FileNotFoundError:
        print(f'파일 {file_path}을 찾을 수 없습니다.')
    except Exception as e:
        print(f'데이터 변환 중 오류가 발생했습니다: {e}')

def main():
    csv_file_path = 'Mars_Base_Inventory_List.csv'
    csv_formet_file_path = 'Mars_Base_Inventory_danger.csv'
    bin_file_path = 'Mars_Base_Inventory_List.bin'

    # Mars_Base_Inventory_List.csv 의 내용을 읽어 들어서 출력한다.
    print('\n-----(csv 내용 출력)-----\n')
    read_csv_print(csv_file_path)

    # Mars_Base_Inventory_List.csv 내용을 읽어서 Python의 리스트(List) 객체로 변환한다.
    inventory_list, header = read_csv_file(csv_file_path)

    # 배열 내용을 적제 화물 목록을 인화성이 높은 순으로 정렬한다.
    inventory_high_flammability_sort = sort_by_flammability(inventory_list)

    # 0.7 이상인 데이터 저장
    high_flammability_data = filter_high_flammability(inventory_list)
    
    print('\n-----(인화성 지수가 0.7 이상 되는 목록)-----\n')
    for i in high_flammability_data:
        print(i)

    write_csv_file(csv_formet_file_path, high_flammability_data, header)
    write_binary_file(bin_file_path, inventory_high_flammability_sort, header)

    print('\n-----(bin 내용 출력)-----\n')
    read_binary_file(bin_file_path)

if __name__ == '__main__':
    main()