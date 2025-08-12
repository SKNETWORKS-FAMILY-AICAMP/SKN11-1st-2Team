import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import matplotlib.font_manager as fm

# 한글 폰트 설정 함수
def set_korean_font():
    font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 '맑은 고딕' 폰트 경로
    plt.rc("font", family=fm.FontProperties(fname=font_path).get_name())

# 한글 폰트 적용
set_korean_font()

def show_excel():
    # 제목
    st.title("📊 시도별 차량 총합 막대 그래프")

    # 파일 경로 설정
    file_path = "Car_list.xlsx"  # 경로 수정

    # Excel 파일 읽기
    try:
        # openpyxl 엔진을 사용하여 엑셀 파일 읽기
        df = pd.read_excel(file_path, engine="openpyxl")

        # 시도별 차량 수 합산 (각 시도가 열(column)로 존재하는 경우)
        시도_목록 = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", 
                 "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]

        # 해당 시도 컬럼이 존재하는 경우만 선택
        df = df[시도_목록].sum()  # 각 시도별 합계 계산

        # NaN 값이 있으면 0으로 변환
        df = df.fillna(0)

        # 막대 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 5))  # 크기를 1000x500으로 설정
        ax.bar(df.index, df.values, color="skyblue")

        # 레이블 및 타이틀 설정
        ax.set_xlabel("시도", fontsize=12)
        ax.set_ylabel("총 차량 수량", fontsize=12)  # y축 레이블을 '총 차량 수량'으로 변경
        ax.set_title("시도별 차량 총합", fontsize=16)
        plt.xticks(rotation=45)  # x축 레이블 회전
        
        # Streamlit에 출력
        st.pyplot(fig)

    except Exception as e:
        st.error(f"파일을 읽는 데 오류가 발생했습니다: {e}")

# Excel 파일 시각화 함수 호출
show_excel()