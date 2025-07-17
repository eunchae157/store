import streamlit as st
import pandas as pd

# 앱 제목
st.title("2025년 5월 연령별 인구 현황 분석")
st.markdown("총인구수 기준 상위 5개 행정구역의 연령별 인구를 선 그래프로 시각화합니다.")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"

# CSV 불러오기
try:
    df = pd.read_csv(file_path, encoding='euc-kr')
    st.success("✅ CSV 파일을 성공적으로 불러왔습니다.")
except Exception as e:
    st.error(f"❌ 파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# 필요한 열만 추출
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
if not age_columns:
    st.error("❌ '2025년05월_계_'로 시작하는 연령별 인구 열을 찾을 수 없습니다.")
    st.stop()

# 연령 숫자만 추출해서 새 이름 만들기
age_labels = [col.replace("2025년05월_계_", "").replace("세", "") for col in age_columns]
age_map = dict(zip(age_columns, age_labels))

# 데이터프레임 정리
df_filtered = df[['행정기관명', '총인구수'] + age_columns].copy()

# 총인구수 기준 상위 5개 지역 추출
top5_df = df_filtered.sort_values(by='총인구수', ascending=False).head(5)

# melt로 세로형으로 변환
df_melted = top5_df.melt(id_vars=['행정기관명'], value_vars=age_columns,
                         var_name='연령', value_name='인구수')

df_melted['연령'] = df_melted['연령'].map(age_map).astype(int)
df_melted = df_melted.sort_values(by='연령')

# 그래프 그리기
st.header("📈 연령별 인구 선 그래프")
for region in df_melted['행정기관명'].unique():
    st.subheader(f"🔹 {region}")
    region_data = df_melted[df_melted['행정기관명'] == region]
    chart_data = region_data.set_index('연령')['인구수']
    st.line_chart(chart_data)

# 원본 데이터 보여주기
st.header("📄 원본 데이터 (상위 5개 행정기관)")
st.dataframe(top5_df)
