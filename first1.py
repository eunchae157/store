import streamlit as st
import pandas as pd

# Streamlit UI 제목
st.title("2025년 5월 연령별 인구 현황 분석")
st.write("📌 총인구수 기준 상위 5개 행정구역의 연령별 인구를 시각화합니다.")

# CSV 파일 경로 및 불러오기 (EUC-KR 인코딩)
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 사용할 열 추출 및 이름 전처리
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_labels = [col.replace("2025년05월_계_", "").replace("세", "") for col in age_cols]
age_map = dict(zip(age_cols, age_labels))

# 필요한 컬럼만 추출
df_filtered = df[['행정기관명', '총인구수'] + age_cols].copy()

# 총인구수 기준 상위 5개 행정기관 선택
top5_df = df_filtered.sort_values(by='총인구수', ascending=False).head(5)

# 연령 데이터를 세로 방향으로 변환 (melt)
df_melted = top5_df.melt(id_vars=['행정기관명'], value_vars=age_cols,
                         var_name='연령', value_name='인구수')

# 연령 컬럼 숫자만 남기고 정렬
df_melted['연령'] = df_melted['연령'].map(age_map).astype(int)
df_melted = df_melted.sort_values(by='연령')

# 그래프 그리기: 각 행정기관별로 연령-인구수 선 그래프 출력
for region in df_melted['행정기관명'].unique():
    st.subheader(f"📈 {region} 연령별 인구 분포")
    region_data = df_melted[df_melted['행정기관명'] == region]
    chart_data = region_data.set_index('연령')['인구수']
    st.line_chart(chart_data)

# 원본 데이터 보여주기
st.subheader("📄 원본 데이터 (상위 5개 행정기관 기준)")
st.dataframe(top5_df)
