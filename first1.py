import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 로드 (업로드 기능 없이 고정)
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 열 추출 및 이름 정리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_age_labels = []
for col in age_columns:
    if '100세 이상' in col:
        new_age_labels.append('100세 이상')
    else:
        new_age_labels.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

# 필요한 데이터프레임 구성
df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_age_labels

# 총인구수 기준 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 원본 데이터 출력
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)

# 선 그래프 출력
st.subheader("📈 상위 5개 행정구역 연령별 인구 분포")
age_columns_only = top5_df.columns[2:]  # 연령별 컬럼들만

for _, row in top5_df.iterrows():
    st.write(f"### {row['행정구역']}")
    age_data = row[age_columns_only].astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
