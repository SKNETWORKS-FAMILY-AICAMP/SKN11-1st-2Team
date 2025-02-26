import urllib.request
import json
import mysql.connector
import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

driver = webdriver.Chrome()

# 캠핑 사이트 이동
driver.get("https://camtayo.com/page/sitemap.php")
time.sleep(1)

# 페이지 끝까지 스크롤 다운
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)  # 스크롤 후 잠시 대기

# "자주하는 질문" 링크 클릭
try:
    faq_link = driver.find_element(By.XPATH, "//div[@class='tt']/a[text()='자주하는 질문']")
    faq_link.click()  # "자주하는 질문" 클릭
    time.sleep(2)  # 클릭 후 페이지 로드 대기
    print("✅ '자주하는 질문' 클릭 완료!")
except Exception as e:
    print(f"❌ '자주하는 질문' 링크를 찾을 수 없음: {e}")

# "내차사기" 링크 클릭
try:
    # "내차사기" 텍스트를 포함하는 a 태그를 찾아 클릭
    car_buy_link = driver.find_element(By.XPATH, "//a[text()='내차사기']")
    car_buy_link.click()  # "내차사기" 클릭
    time.sleep(2)  # 클릭 후 페이지 로드 대기
    print("✅ '내차사기' 클릭 완료!")
except Exception as e:
    print(f"❌ '내차사기' 링크를 찾을 수 없음: {e}")

# 캠핑카 관련 질문과 답변 추출
faq_items = driver.find_elements(By.XPATH, "//dt[contains(text(), '캠타요')]")  # 캠타요와 관련된 질문을 찾음
faq_data = []
for item in faq_items:
    try:
        question = item.text.strip()

        # 질문에 맞는 답변을 추출하는 부분 수정 (답변이 다른 XPath 구조일 수 있음)
        answer_element = item.find_element(By.XPATH, "following-sibling::dd")  # 기존 XPath
        answer = answer_element.text.strip()

        faq_data.append((question, answer))
    except Exception as e:
        print(f"❌ 질문 또는 답변 추출 중 오류 발생: {e}")

# 출력된 faq_data 확인
print(f"추출된 질문과 답변: {faq_data}")

# MySQL 연결
connection = get_connection()
cursor = connection.cursor()

# 테이블 생성 (car_camping_faq)
create_table_query = """
CREATE TABLE IF NOT EXISTS car_camping_faq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    answer TEXT NOT NULL
);
"""
cursor.execute(create_table_query)
connection.commit()

# 질문과 답변 데이터 삽입
insert_query = """
INSERT INTO car_camping_faq (question, answer)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE 
    answer = VALUES(answer);
"""

# MySQL 데이터 삽입
cursor.executemany(insert_query, faq_data)
connection.commit()

print(f"{len(faq_data)} rows inserted or updated successfully in the database.")

# CSV 파일 경로
csv_filename = "car_camping_faq.csv"

# CSV 파일에 저장하기 전에 기존 질문들을 확인
existing_questions = set()

# 기존 CSV 파일이 존재하면 질문을 읽어와서 중복 방지
if os.path.exists(csv_filename):
    existing_df = pd.read_csv(csv_filename, encoding='utf-8-sig')
    existing_questions.update(existing_df["질문"].tolist())

# 중복을 제거한 데이터 리스트 생성
filtered_data = [
    (question, answer)
    for question, answer in faq_data
    if question not in existing_questions
]

# 데이터가 있으면 pandas DataFrame으로 변환하여 CSV로 저장
if filtered_data:
    df = pd.DataFrame(filtered_data, columns=["질문", "답변"])

    # CSV에 저장 (헤더가 없으면 추가)
    df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False, encoding='utf-8-sig')

    print(f"📁 CSV 저장 완료: {csv_filename}")
else:
    print("⚠️ 중복된 질문이 있어 CSV에 저장되지 않았습니다.")

# 연결 종료
cursor.close()
connection.close()
