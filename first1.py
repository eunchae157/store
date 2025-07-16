import streamlit as st
import pandas as pd

# CSV 파일 불러오기 (EUC-KR 인코딩)
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

st.title("2025년 5월 기준 연령별 인구 현황 분석")
st.write("총인구수 기준 상위 5개 행정구역의 연령별 인구 분포를 선 그래프로 확인할 수 있습니다.")

# 열 이름 전처리: '2025년05월_계_'로 시작하는 열에서 연령만 추출
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
ages = [col.replace("2025년05월_계_", "").replace("세", "") for col in age_cols]
age_map = dict(zip(age_cols, ages))

# '총인구수'와 연령별 열만 추출
df_trimmed = df[['행정기관명', '총인구수'] + age_cols].copy()

# 총인구수 기준 상위 5개 행정기관만 선택
top5 = df_trimmed.sort_values(by='총인구수', ascending=False).head(5)

# 데이터 시각화를 위해 형식 변환
df_melted = top5.melt(id_vars=['행정기관명'], value_vars=age_cols,
                      var_name='연령', value_name='인구수')
df_melted['연령'] = df_melted['연령'].map(age_map)
df_melted['연령'] = df_melted['연령'].astype(int)
df_melted = df_melted.sort_values(by='연령')

# 행정기관별로 데이터 분리 및 그래프 출력
for region in df_melted['행정기관명'].unique():
    st.subheader(f"📊 {region}의 연령별 인구 추이")
    region_data = df_melted[df_melted['행정기관명'] == region]
    region_data_sorted = region_data.sort_values('연령')
    region_chart = region_data_sorted.set_index('연령')['인구수']
    st.line_chart(region_chart)

# 원본 데이터 표시
st.subheader("📄 원본 데이터 (상위 5개 행정기관 기준)")
st.dataframe(top5)
