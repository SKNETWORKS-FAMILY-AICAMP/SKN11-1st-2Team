import streamlit as st
from page.home import show_home
from page.excel import show_excel
from page.plus import show_plus
from page.faq import show_faq

import mysql.connector

# MySQL 연결 함수
@st.cache_resource  # 캐싱하여 매번 새 연결을 만들지 않도록 최적화
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="car",
            password="car",
            database="cardb"
        )
        return connection
    except mysql.connector.Error as e:
        st.error(f"MySQL 연결 실패: {e}")
        return None

# 제목
st.title("특수차 등록 현황 및 기업 FAQ 조회 시스템")

# 사이드바 메뉴 만들기
menu = st.sidebar.radio("🗂️ 메뉴", ["🏠 홈", "📜 엑셀 업로드", "🚩 추가 정보", "🤔 질문!"])

# MySQL 연결 확인 버튼 추가 (선택 사항)
if st.sidebar.button("🔌 MySQL 연결 확인"):
    conn = get_connection()
    if conn and conn.is_connected():
        st.success("✅ MySQL에 정상 연결되었습니다.")
        conn.close()  # 연결 닫기
    else:
        st.error("❌ MySQL 연결에 실패했습니다.")

# 각 메뉴에 따른 화면 표시
if menu == "🏠 홈":
    show_home()
elif menu == "📜 엑셀 업로드":
    show_excel()
elif menu == "🚩 추가 정보":
    show_plus()
elif menu == "🤔 질문!":
    show_faq()
