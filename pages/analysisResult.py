import streamlit as st
import pandas as pd
from PIL import Image

def main():
    # Set page config
    st.set_page_config(
        page_title="EDA Result",
        layout="wide"
    )

    st.title("Slack 운영 데이터 분석 결과")

    # sidebar
    # 이미지 파일 불러오기
    image = Image.open('assets\images\logo_slack.png')

    st.sidebar.image(image)
    st.sidebar.write("Slack Channels")

    # Content / Row 1
    with st.container(border=True):
       st.write("일별 데이터 전송량") 

    # Content / Row 2
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.write("최대 전송량")
    
    with col2:
        with st.container(border=True):
            st.write("메시지 평균 응답 시간")
    
    with col3:
        with st.container(border=True):
            st.write("메시지 평균 처리 시간")
    
    # Content / Row 3
    col4, col5 = st.columns(2)
    
    with col4:
        with st.container(border=True):
            st.write("주요 키워드")
    
    with col5:
        with st.container(border=True):
            st.write("추가 예정")

    # # 업로드된 데이터가 세션 상태에 있는지 확인
    # if 'uploaded_data' in st.session_state:
    #     df = st.session_state['uploaded_data']
    #     st.dataframe(df)
    # else:
    #     st.write("No data uploaded.")

if __name__ == "__main__":
    main()