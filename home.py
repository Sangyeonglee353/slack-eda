import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from wordcloud import WordCloud

# Set page config
st.set_page_config(
    page_title="Slack 운영 데이터 시각화 대시보드",
    layout="wide"
)

# 이미지 파일 불러오기
image = Image.open('assets\images\logo_slack.png')

def image_to_base64(image):
    import base64
    from io import BytesIO
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# 이미지 정가운데 배치 HTML/CSS 코드
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    .center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 50vh;  /* 뷰포트 높이를 채웁니다 */
    }
    .title {
        color: black;
        font-size: 24px;
        margin-top: 20px;
        font-weight: bold;
    }
    .content {
        margin-top: 20px;
        text-align: center;
    }
    .content-title {
        color: black;
        font-size: 18px;
        margin-top: 20px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 정가운데 배치된 이미지 출력
st.markdown(f'''<div class="center">
            <img src="data:image/png;base64,{image_to_base64(image)}" width="300">
            <div class="title">Slack 과정 운영 데이터 분석</div>
            <div class="content">
                <div class="content-title">운영 중이신 과정의 Slack 데이터(.json)를 추출하여 삽입해주세요.</div>
            </div>
            </div>''', unsafe_allow_html=True)

# File uploader를 중앙에 배치

uploaded_files = st.file_uploader("운영 중이신 과정의 Slack 데이터(.json)를 추출하여 삽입해주세요.", type=['json'], accept_multiple_files=True)