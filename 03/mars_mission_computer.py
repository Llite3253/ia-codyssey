import random

class DummySensor:
    # init 메소드는 객체 생성 시 초기값 설정을 위해 자동 호출되는 생성자자
    def __init__(self):
        self.env_values = {
            # None을 쓰는 이유: py 에서는 값을 초기화 되지 않은 상태를 나타내기 위해 None을 사용
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
    
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 2)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def get_env(self):
        month = random.randint(1, 12)
        if month in (1, 3, 5, 7, 8, 10, 12) :
            day = random.randint(1, 31)
        elif month in (4, 6, 9, 11):
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        timestamp = '2025-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(month, day, hour, minute, second)

        log_line = (
            timestamp + ', ' +
            'mars_base_internal_temperature: ' + str(self.env_values.get('mars_base_internal_temperature')) + ', ' +
            'mars_base_external_temperature: ' + str(self.env_values.get('mars_base_external_temperature')) + ', ' +
            'mars_base_internal_humidity: ' + str(self.env_values.get('mars_base_internal_humidity')) + ', ' +
            'mars_base_external_illuminance: ' + str(self.env_values.get('mars_base_external_illuminance')) + ', ' +
            'mars_base_internal_co2: ' + str(self.env_values.get('mars_base_internal_co2')) + ', ' +
            'mars_base_internal_oxygen: ' + str(self.env_values.get('mars_base_internal_oxygen')) + '\n'
        )
        try:
            with open('env.log', 'a') as log_file:
                log_file.write(log_line)
        except Exception as e:
            print('로그 파일 저장 오류: ', e)
        return self.env_values

def main():
    ds = DummySensor()
    ds.set_env()
    env = ds.get_env()
    print('환경 값:')
    for key, value in env.items():
        if key == 'mars_base_internal_temperature' or key == 'mars_base_external_temperature':
            print('{0}: {1}도'.format(key, value))
        elif key == 'mars_base_internal_humidity' or key == 'mars_base_internal_co2' or key == 'mars_base_internal_oxygen':
            print('{0}: {1}%'.format(key, value))
        elif key == 'mars_base_external_illuminance':
            print('{0}: {1} W/m2'.format(key, value))

if __name__ == '__main__':
    main()