import streamlit as st

# 페이지 기본 설정.
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

# CSS 스타일을 적용한 HTML 코드
css_html = """
<style>
.centered {
    text-align: center;
    margin: 0 auto;
    max-width: 800px;  /* 페이지의 최대 너비를 조절할 수 있습니다. */
}
.centered-header {
    font-size: 36px;
    margin-top: 30px;
}
.centered-subheader {
    font-size: 24px;
    margin-top: 20px;
    margin-bottom: 30px;
}
.centered-text {
    font-size: 18px;
    margin-top: 30px;
}
</style>
"""

# HTML 코드 렌더링
st.markdown(css_html, unsafe_allow_html=True)
st.markdown("""
<div class="centered">
    <div class="centered-header">차량 렌더링 및 제원 정보 확인 서비스</div>
    <div class="centered-subheader"> </div>
    <div class="centered-text">
        최신 기술인 NeRF (Neural Radiance Fields)를 활용하여 차량 시각화 및 제원 정보 서비스를 제공합니다. 이 서비스는 사용자로부터 몇 장의 이미지를 입력 받아, 해당 차량의 종류, 제원, 평균 중고 가격 등을 제공합니다. 기존 렌더링과 달리 현실적이며 고품질의 3D 시각화를 통해 디자인, 마케팅, 엔지니어링 등 다양한 분야에서 활용할 수 있습니다.
    </div>
</div>
""", unsafe_allow_html=True)

# 이미지를 sidebar에 추가
st.sidebar.image(banner_image_url, width=200)

# 렌더링 결과 설명
st.markdown("""
<div class="centered">
    <h2>사용방법</h2>
    <p>사용방법은 다음과 같습니다.</p>
    <ol>
        <li><strong>차종 검색</strong>: 차량의 종류, 제원, 시세 등을 확인하려면 자동차 사진을 찍어 업로드하십시오.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="centered">
    <h2>렌더링 결과</h2>
    <p>본 서비스에서 제공하는 렌더링 결과는 다음과 같습니다.</p>
    <ol>
        <li><strong>차량 시각화</strong>: 입력한 이미지를 기반으로 NeRF (Neural Radiance Fields) 모델을 사용하여 차량의 3D 시각화를 생성합니다.</li>
        <li><strong>제원 정보</strong>: 생성된 차량 모델의 제원 정보를 표시합니다. 이 정보에는 차량의 길이, 너비, 높이, 최대 마력 등이 포함될 수 있습니다.</li>
        <li><strong>가격</strong>: 해당 차량의 가격을 제공합니다. 이 정보는 참고용으로만 사용되며 실제 가격과 다를 수 있습니다.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="centered">
    <h2>서비스 이용 안내</h2>
    <p>본 서비스 이용 안내는 다음과 같습니다.</p>
    <ol>
        <li>본 서비스는 NeRF 모델을 사용하여 차량 렌더링과 제원 정보를 제공합니다.</li>
        <li>입력한 이미지의 품질에 따라 결과물의 품질이 달라질 수 있습니다.</li>
        <li>평균 중고 가격 정보는 시장 조사를 기반으로 제공되며 참고용으로만 사용하세요.</li>
        <li>서비스 이용 중 문제가 발생하면 고객 지원팀에 문의하세요.</li>
    </ol>
    <p>더 자세한 정보나 지원이 필요한 경우, <a href="mailto:kshihk7983@gmail.com">고객 지원팀에 문의</a>하세요.</p>
</div>
""", unsafe_allow_html=True)