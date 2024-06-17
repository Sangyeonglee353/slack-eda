import streamlit as st
import pandas as pd
from PIL import Image
import os
import json

def main():
    # Set page config
    st.set_page_config(
        page_title="EDA Result",
        layout="wide"
    )

    st.title("Slack 운영 데이터 분석 결과")

    # sidebar
    # 이미지 파일 불러오기
    image = Image.open('../assets/images/logo_slack_white.png')

    st.sidebar.image(image)

    # getData
    # 폴더 및 채널 가져오기
    # folders > folder > channel > daily
    folders_path = "../data/"
    if os.path.exists(folders_path) and os.path.isdir(folders_path):
        folders = os.listdir(folders_path)
        selected_folder = st.sidebar.selectbox("Select a BootCamp", options=folders)
        folder_path = os.path.join(folders_path, selected_folder)
        channels = os.listdir(folder_path)
        filtered_channels = [channel for channel in channels if 'json' not in channel]
        # selected_channel = st.sidebar.radio("Channel list", options=filtered_channels)
        # 버튼 클릭 이벤트 처리
        for channel in filtered_channels:
            if st.sidebar.button(channel):
                st.session_state['selected_channel'] = channel

    # 선택된 채널 로드
    if 'selected_channel' in st.session_state:
            channel_path = os.path.join(folder_path, st.session_state['selected_channel'])
            if os.path.isdir(channel_path):
                files = os.listdir(channel_path)
                jsonDataList = []
                fileNameList = []
                for file_name in files:
                    if file_name.endswith('.json'):
                        file_path = os.path.join(channel_path, file_name)
                        with open(file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            # st.write(f"Data from {file_name}: {data}")
                            convertFilename = file_name.replace(".json", "")
                            jsonData = {"date": convertFilename, "value": data}
                            jsonDataList.append(jsonData)
                            fileNameList.append(convertFilename)
                            fileNameList.sort()
                st.write("success!")
                st.write(fileNameList)
            else:
                st.error("선택한 채널의 데이터 파일이 존재하지 않습니다.")

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