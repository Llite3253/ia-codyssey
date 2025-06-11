import csv
import mysql.connector
from datetime import datetime

class MySQLHelper:
    def __init__(self, host='localhost', port='3307', user='root', password='', database='mars'):
        self.conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def insert_weather(self, weather_id, mars_date, temp, storm):
        query = (
            'INSERT INTO mars_weather (weather_id, mars_date, temp, storm) '
            'VALUES (%s, %s, %s, %s)'
        )
        self.cursor.execute(query, (weather_id, mars_date, temp, storm))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


def load_weather_data_from_csv(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            try:
                weather_id = int(row['weather_id'])
                mars_date = datetime.strptime(row['mars_date'], '%Y-%m-%d')
                temp = float(row['temp'])
                storm = int(row['storm'])
                data.append((weather_id, mars_date, temp, storm))
            except Exception as e:
                print('⚠️ 잘못된 행:', row, e)
        return data


def insert_data_to_db(data):
    db = MySQLHelper()
    for weather_id, mars_date, temp, storm in data:
        db.insert_weather(weather_id, mars_date, temp, storm)
    db.close()


if __name__ == '__main__':
    csv_file_path = './03_problem_01_05/mars_weathers_data.csv'
    weather_data = load_weather_data_from_csv(csv_file_path)
    insert_data_to_db(weather_data)
    print(f'✅ 총 {len(weather_data)}건의 데이터를 DB에 저장했습니다.')
