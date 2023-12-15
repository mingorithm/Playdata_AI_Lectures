import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(
    page_icon="🚘",
    page_title="차량 렌더링 및 제원 정보 확인 서비스",
    layout="wide",
)

# 배너 이미지 추가를 위한 HTML 스타일 코드
banner_style = """
    <style>
        .banner-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 300px;  # 원하는 높이로 조정하세요.
        }
        .banner-img {
            max-width: 100%;
        }
    </style>
"""

# 배너 이미지 출력
banner_image_url = 'https://ifh.cc/g/vbmRgR.jpg'
st.markdown('<p style="text-align:center;"><img src="%s" alt="Banner Image" width="800"></p>' % banner_image_url, unsafe_allow_html=True)

st.info('🚘 조회 가능 차량 List')

data = {
    '차종' : ["MAXCRUZ", "MORNING", "SONATA", "TIVOLI", "SM5", "STINGER", "MOHAVE", "CARNIVAL", "TUCSON", "CLIO"],
    '연식' : ['2017 ~ 2018', '2017 ~ 2021', '2017 ~ 2021', '2017 ~ 2021', '2017 ~ 2020', '2017 ~ 2021', '2017 ~ 2021', '2017 ~ 2021', '2017 ~ 2021', '2017 ~ 2021']
    }
df = pd.DataFrame(data)
st.dataframe(df, width=800)

st.info('🚘 차량 제원')

# DBeaverFH 데이터베이스 연결 설정
def create_conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="zasx1452",
        database="sys"
    )
    return conn

def run_query(query):
    conn = create_conn()
    df = pd.read_sql_query(query,conn)
    return df

query = "select * from car_infos"
df = run_query(query)
st.write(df)

st.sidebar.title('차량 추천 받기 🌸')
car_info = st.sidebar.multiselect(
    '추천 받고 싶은 차량을 고르시요, 복수 선택 가능',
    ["TIVOLI", "PALISADE", "PORTER2", "i30", "G4 REXTON", "K3", "K5", "K7", "K9", "QM3", "QM6", "SM3",
                        "SM5", "SM6", "SM7", "XM3", "GRANDEUR", "NIRO", "DAMAS", "RAY", "REXTON SPORT", "MAXCRUZ",
                        "MORNING", "MOHAVE", "VENUE", "VELOSTER", "BONGO3", "SELTOS", "STAREX", "STONIC", "STINGER",
                        "SPORTAGE", "SANTAFE", "SONATA", "SORENTO", "SOUL", "AVANTE", "IONIQ", "ACCENT", "CARNIVAL",
                        "KONA", "KORANDO", "KORANDO TURISMO", "KORANDO C", "TUCSON", "CLIO"]
)
st.info('🚘 차량 비교 하기')
tmp_df = df[df['차종'].isin(car_info)]
st.table(tmp_df.head())

car_infos = ["TIVOLI", "PALISADE", "PORTER2", "i30", "G4 REXTON", "K3", "K5", "K7", "K9", "QM3", "QM6", "SM3",
                        "SM5", "SM6", "SM7", "XM3", "GRANDEUR", "NIRO", "DAMAS", "RAY", "REXTON SPORT", "MAXCRUZ",
                        "MORNING", "MOHAVE", "VENUE", "VELOSTER", "BONGO3", "SELTOS", "STAREX", "STONIC", "STINGER",
                        "SPORTAGE", "SANTAFE", "SONATA", "SORENTO", "SOUL", "AVANTE", "IONIQ", "ACCENT", "CARNIVAL",
                        "KONA", "KORANDO", "KORANDO TURISMO", "KORANDO C", "TUCSON", "CLIO"]
# 선택한 내용을 radio_select 변수에 담습니다
radio_select = st.sidebar.radio(
    "비교 대상을 선택하시요.",
    ['가격', '연비', '출력'],
    horizontal=True
)
# 선택한 컬럼에 따라 slider_range 값을 다르게 설정
if radio_select == '가격':
    # 가격에 따른 범위 설정
    slider_range = st.sidebar.slider(
        "choose range of 가격 column",
        0,  # 시작 값
        10000,  # 끝 값
        (1000, 5000)  # 기본값, 앞 뒤로 2개 설정
    )
elif radio_select == '연비':
    slider_range = st.sidebar.slider(
        "choose range of 연비 column",
        0,
        50,
        (10, 40)
    )
elif radio_select == '출력':
    slider_range = st.sidebar.slider(
        "choose range of 출력 column",
        0,
        500,
        (50, 300)
    )
start_button = st.sidebar.button("Filter Apply 📊")

if start_button:
    # 선택한 차종들로 데이터프레임을 필터링
    tmp_dfs = df[df['차종'].isin(car_infos)].copy()
    price_range = tmp_dfs['가격'].str.split('~')
    prices = price_range.apply(lambda x: [int(val.replace(',', '').replace('만원', '').replace('달러', '')) if val else 0 for val in x])

    # 가격 범위의 최소값과 최대값을 별도의 열에 저장
    tmp_dfs['가격_최소'] = prices.apply(lambda x: x[0])
    tmp_dfs['가격_최대'] = prices.apply(lambda x: x[1] if len(x) > 1 else x[0])
    tmp_dfs['연비'] = tmp_dfs['연비'].str.extract('(\d+\.?\d*)', expand=False).astype(float)
    tmp_dfs['출력'] = tmp_dfs['출력'].str.extract('(\d+\.?\d*)', expand=False).astype(int)

    # 선택한 컬럼에 따라 필터링 조건 설정
    filter_condition = None
    if radio_select == '가격':
        filter_condition = (tmp_dfs['가격_최소'] >= slider_range[0]) & (tmp_dfs['가격_최대'] <= slider_range[1])
    elif radio_select == '연비':
        filter_condition = (tmp_dfs['연비'] >= slider_range[0]) & (tmp_dfs['연비'] <= slider_range[1])
    elif radio_select == '출력':
        filter_condition = (tmp_dfs['출력'] >= slider_range[0]) & (tmp_dfs['출력'] <= slider_range[1])

    # 원본 데이터에서 필터링된 행을 다시 선택하여 출력
    output_df = df.loc[tmp_dfs[filter_condition].index]
    st.info('🚘 차량 조건 비교 하기')
    st.table(output_df)

image_url = "https://ifh.cc/g/vbmRgR.jpg"
# 이미지를 sidebar에 추가
st.sidebar.image(image_url, width=200)