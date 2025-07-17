import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ----------------------------
# 📍 위도/경도 수동 매핑 (필요한 만큼 추가 가능)
# ----------------------------
location_dict = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '인천광역시': [37.4563, 126.7052],
    '대구광역시': [35.8722, 128.6025],
    '경기도': [37.4138, 127.5183],
    # 필요한 행정구역은 계속 추가 가능
}

# ----------------------------
# 🔹 데이터 불러오기
# ----------------------------
st.title("2025년 5월 기준 연령별 인구 지도 시각화")

df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령 컬럼 필터링
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_age_labels = []
for col in age_columns:
    if '100세 이상' in col:
        new_age_labels.append('100세 이상')
    else:
        new_age_labels.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_age_labels

# 상위 5개 지역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# ----------------------------
# 🌍 지도 생성 및 마커 표시
# ----------------------------
m = folium.Map(location=[36.5, 127.9], zoom_start=7)

for _, row in top5_df.iterrows():
    region = row['행정구역']
    population = row['총인구수']
    
    if region in location_dict:
        lat, lon = location_dict[region]
        
        folium.CircleMarker(
            location=(lat, lon),
            radius=population / 1000000,  # 인구수에 비례한 크기
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.4,
            popup=f"{region} ({population:,}명)"
        ).add_to(m)

# ----------------------------
# 📍 지도 출력
# ----------------------------
st.subheader("🗺️ 상위 5개 행정구역 인구 분포 지도")
st_data = st_folium(m, width=700, height=500)

# ----------------------------
# 📄 원본 데이터 함께 표시
# ----------------------------
st.subheader("📊 상위 5개 행정구역 원본 데이터")
st.dataframe(top5_df)
