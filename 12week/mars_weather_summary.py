import csv
import pymysql

class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def execute_update(self, query, args=None):
        self.cursor.execute(query, args)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

def main():
    # ⚠️ 본인의 MySQL 비밀번호와 DB 이름으로 다시 변경해 주세요!
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'zlekfl8901' 
    db_name = 'mars_db' 

    print('--- 화성 날씨 데이터베이스 작업 시작 ---')

    try:
        db_helper = MySQLHelper(db_host, db_user, db_password, db_name)
        
        # 1. 테이블 생성 (요구사항대로 temp, storm은 INT)
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS mars_weather (
                weather_id INT AUTO_INCREMENT PRIMARY KEY,
                mars_date DATETIME NOT NULL,
                temp INT,
                storm INT
            )
        '''
        db_helper.execute_update(create_table_query)
        print('테이블(mars_weather) 확인 및 생성 완료.')

        # 2. CSV 파일 읽기 및 DB 삽입
        csv_file_path = 'mars_weathers_data.csv'
        insert_query = '''
            INSERT INTO mars_weather (mars_date, temp, storm)
            VALUES (%s, %s, %s)
        '''
        insert_count = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader, None)
            
            for row in csv_reader:
                if row:
                    mars_date = row[1]
                    
                    # 💡 해결된 부분: '21.4' 같은 소수점 문자열을 float로 먼저 바꾼 뒤 int로 변환 (소수점은 버려짐)
                    temp = int(float(row[2]))     
                    storm = int(float(row[3]))    
                    
                    db_helper.execute_update(insert_query, (mars_date, temp, storm))
                    insert_count += 1
                    
        print(f'총 {insert_count}개의 날씨 데이터가 성공적으로 백업되었습니다.')
        
        db_helper.close()
        print('--- 데이터베이스 연결 종료 ---')
        
    except FileNotFoundError:
        print('오류: mars_weathers_data.csv 파일을 찾을 수 없습니다.')
    except pymysql.MySQLError as e:
        print(f'MySQL 처리 중 오류가 발생했습니다: {e}')
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')

if __name__ == '__main__':
    main()