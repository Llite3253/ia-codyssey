import platform  # 시스템 정보
import psutil  # 시스템 자원 사용량

class MissionComputer:
    def __print_json(self, data):
        # 주어진 데이터를 JSON 형태로 출력
        json_str = '{\n'
        for key, value in data.items():
            json_str += f'    "{key}": {value},\n'
        json_str = json_str.rstrip(',\n') + '\n}'
        print(json_str)

    def __load_settings(self):
        try:
            with open('setting.txt', 'r') as file:
                settings = [line.strip() for line in file.readlines()]
            return settings
        except FileNotFoundError:
            print('setting.txt 파일이 없습니다. 모든 정보를 출력합니다.')
            return None

    def get_mission_computer_info(self):
        settings = self.__load_settings()
        try:
            system_info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                # logical=False: 실제 cpu 하드웨어 정보를 얻을 때
                'cpu_cores': psutil.cpu_count(logical=False),
                # 바이트 단위로 나오기 때문에
                'memory_size_gb': round(psutil.virtual_memory().total / (1024**3), 2)
            }
        except Exception as e:
            print(f'시스템 정보 조회 중 예외 발생: {e}')
        if settings:
            system_info = {k: v for k, v in system_info.items() if k in settings}
        self.__print_json(system_info)

    def get_mission_computer_load(self):
        try:
            load_info = {
                # interval: 어떤 값을 측정할 때 사용하는 시간 간격
                'cpu_usage_percent': psutil.cpu_percent(interval=1),
                'memory_usage_percent': psutil.virtual_memory().percent
            }
            self.__print_json(load_info)
        except Exception as e:
            print(f'시스템 부하 조회 중 에러 발생: {e}')

if __name__ == '__main__':
    runComputer = MissionComputer()

    # 시스템 정보 출력 테스트
    print('--- Mission Computer Info ---')
    runComputer.get_mission_computer_info()

    # 시스템 부하 출력 테스트
    print('\n--- Mission Computer Load ---')
    runComputer.get_mission_computer_load()
