import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from wordcloud import WordCloud

import os

def main():
    # Set page config
    st.set_page_config(
        page_title="Slack Dashboard",
        layout="wide"
    )

    # 이미지 파일 불러오기
    image = Image.open('../assets/images/logo_slack.png')

    def image_to_base64(image):
        import base64
        from io import BytesIO
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    # 이미지 정가운데 배치 HTML/CSS 코드
    # CSS 스타일 적용
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        .center {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 50vh; /* 뷰포트 높이를 채웁니다 */
        }
        .title {
            color: black;
            font-size: 24px;
            margin-top: 20px;
            font-weight: bold;
            text-align: center;
        }
        .content {
            width: 70%;
            /* margin-top: 20px; */
            margin-bottom: 20px;
            text-align: center;
            /*
            background-color: #D9D9D9;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px; */
        }
        .content-title {
            color: black;
            font-size: 18px;
            margin-top: 20px;
            font-weight: bold;
        }
        .content-title__sub {
            color: black;
            font-size: 16px;
            margin-top: 10px;
        }
        [data-testid='stFileUploader'] {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        [data-testid='stFileUploaderDropzone'] {
            width: 60%;
        }
        [data-testid='stFileUploaderDropzone'] {
            width: 60%;
        }
        [data-testId='stMarkdownContainer'] > p{
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 정가운데 배치된 이미지 출력
    with st.container(border=True):
        st.markdown(f'''
        <div class="center">
            <img src="data:image/png;base64,{image_to_base64(image)}" width="500">
            <div class="title">Slack 과정 운영 데이터 분석</div>
            <div class="content">
                <div class="content-title">운영 중인 과정의 Slack 데이터(.json)를 추출하여 삽입해주세요.</div>
                <div class="content-title__sub">< 추출 방법 가이드(노션_링크) ></div>
            </div>
        </div>    
        ''', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("json_data", type=['json'], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # 파일 내용 읽기
            data = pd.read_json(uploaded_file)
            df = pd.json_normalize(data)
            st.write(df)

    ## 단일 파일
    # uploaded_file = st.file_uploader("json_data", type=['json'], accept_multiple_files=False)

    # # 업로드된 파일 처리 및 페이지 전환
    # if uploaded_file:
    #     st.markdown(f'''<div class="title">There is File</div>''', unsafe_allow_html=True)
    #     # st.switch_page('analysisResult')
    #     # if 'uploaded_data' not in st.session_state:
    #     data = pd.read_json(uploaded_file)
    #     df = pd.json_normalize(data)

    #     # 페이지 전환을 위해 세션 상태를 업데이트하고 리디렉션
    #     st.session_state['uploaded_data'] = df
    #     st.session_state['page'] = 'analysisResult'
    #     st.switch_page('pages/analysisResult.py')
        
    # 폴더 가져오기
    # folders > folder > channels > channel
    folders_path = "../data/"
    if folders_path:
        if os.path.exists(folders_path) and os.path.isdir(folders_path):
            # 폴더 내의 파일 목록을 가져오기
            folders = os.listdir(folders_path)
            if folders:
                # st.write("폴더 내 파일 목록:")
                st.write(folders)
                folder_path = folders_path + folders[0]
                folder = os.listdir(folder_path)
                st.write(folder)
                
                
            else:
                st.write("폴더가 비어 있습니다.")

    else:
        st.session_state['page'] = 'home'

if __name__ == "__main__":
    main()