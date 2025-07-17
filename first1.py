import streamlit as st
import pandas as pd

# CSV 파일 불러오기
file_path = '202505_202505_연령별인구현황_월간.csv'
df = pd.read_csv(file_path, encoding='euc-kr')

st.title("2025년 5월 연령별 인구 현황 분석")
st.write("이 앱은 2025년 5월 기준 연령별 인구 현황을 분석하여 상위 5개 행정구역의 인구 분포를 시각화합니다.")

# 열 이름 전처리
original_columns = df.columns.tolist()
age_columns = [col for col in original_columns if col.startswith("2025년05월_계_")]
age_labels = [col.replace("2025년05월_계_", "") for col in age_columns]

# 총인구수 기준 상위 5개 지역 추출
df_top5 = df.nlargest(5, '총인구수')

# 연령 데이터만 추출 후 전치 (Transpose)
age_df = df_top5[["행정구역"] + age_columns].copy()
age_df.columns = ["행정구역"] + age_labels
age_df = age_df.set_index("행정구역").T  # 연령을 인덱스로

st.subheader("상위 5개 행정구역 연령별 인구 분포 (선 그래프)")
st.line_chart(age_df)

st.subheader("원본 데이터 (일부 열 생략 가능)")
st.dataframe(df)
