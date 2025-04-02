import random
import time

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        self.env_values = {
            'mars_base_internal_temperature': random.randint(18, 30),
            'mars_base_external_temperature': random.randint(0, 21),
            'mars_base_internal_humidity': random.randint(50, 60),
            'mars_base_external_illuminance': random.randint(500, 715),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 2),
            'mars_base_internal_oxygen': random.randint(4, 7)
        }

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        # DummySensor 클래스 인스턴스 생성
        self.ds = DummySensor()
        # 환경 값을 가져와 초기화
        self.env_values = self.ds.get_env()
        # 환경 데이터 누적 합산을 위한 딕셔너리 초기화
        self.env_sums = {key: 0 for key in self.env_values}
        # 데이터 수집 횟수 초기화
        self.readings_count = 0
        # 평균 계산 시작 시간 기록
        self.start_time = time.time()

    def print_json(self, data):
        # 주어진 데이터를 JSON 형태로 출력
        print('{')
        for key, value in data.items():
            print(f'    "{key}": {value},')
        print('}')

    def update_env_sums(self):
        # 각 환경 데이터를 누적 합산
        for key in self.env_values:
            self.env_sums[key] += self.env_values[key]
        # 데이터 수집 횟수 증가
        self.readings_count += 1

    def calculate_and_print_average(self):
        # 5분간 누적된 데이터 평균 계산 및 출력
        averages = {
            key: round(self.env_sums[key] / self.readings_count, 2)
            for key in self.env_values
        }
        print('\n5분 평균 값:')
        self.print_json(averages)

        # 평균값 출력 후 누적 데이터 초기화
        self.env_sums = {key: 0 for key in self.env_values}
        self.readings_count = 0
        # 평균 계산 시간 리셋
        self.start_time = time.time()

    def get_sensor_data(self):
        # 센서 데이터 주기적으로 수집, 추력, 평균 계산 반복
        try:
            while True:
                self.ds.set_env() # 센서 데이터 랜덤 설정
                self.env_values = self.ds.get_env() # 설정된 데이터 가져오기

                self.print_json(self.env_values) # 현재 환경 데이터 출력

                self.update_env_sums() # 평군 계산을 위한 데이터 누적

                # 5분마다 평균값 계산 및 출력
                if time.time() - self.start_time >= 300:
                    self.calculate_and_print_average()

                time.sleep(5)

        except KeyboardInterrupt:
            # 반복 중단 (Ctrl+C 입력 시 실행)
            print('\nSystem stopped....')


if __name__ == '__main__':
    # MissionComputer 클래스 인스턴스 생성 및 실행
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
