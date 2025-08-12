import urllib.request
import json 
import mysql.connector

# MySQL 연결 함수
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="car",
        password="car",
        database="cardb"
    )

client_id = 'ravTGA6TIfjD6VIOBdjM'
client_secret = '3R4dvUUiuj'

# 검색어 설정
searchText = urllib.parse.quote('캠핑카')


# API 요청 URL 및 헤더 설정
url = f"https://openapi.naver.com/v1/search/news.json?query={searchText}&display=100"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

# API 요청 및 JSON 변환
response = urllib.request.urlopen(request)
response_body = response.read()
response_body = json.loads(response_body)

# 뉴스 데이터 가져오기
news_list = response_body.get('items', [])

# MySQL 연결
connection = get_connection()
cursor = connection.cursor()

# 테이블 생성 (필요 시)
create_table_query = """
CREATE TABLE IF NOT EXISTS special_vehicle_news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    link VARCHAR(500) UNIQUE,
    description TEXT,
    pub_date VARCHAR(50)
);
"""
cursor.execute(create_table_query)
connection.commit()

# 뉴스 데이터 삽입
insert_query = """
INSERT INTO special_vehicle_news (title, link, description, pub_date)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    title = VALUES(title),
    description = VALUES(description),
    pub_date = VALUES(pub_date);
"""

news_data = [
    (news['title'], news['link'], news['description'], news['pubDate'])
    for news in news_list
]

cursor.executemany(insert_query, news_data)
connection.commit()

print(f"{len(news_data)} rows inserted or updated successfully.")

# 연결 종료
cursor.close()
connection.close()