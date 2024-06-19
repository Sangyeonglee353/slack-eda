import streamlit as st
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import json
import re
import plotly.express as px

def main():
    # Set page config
    st.set_page_config(
        page_title="EDA Result",
        layout="wide"
    )

    st.title("운영 데이터 분석 결과")

##############################################
    # sidebar
    # 이미지 파일 불러오기
    image = Image.open('../assets/images/logo_slack_white.png')

    st.sidebar.image(image)

    # getData
    # 1. 폴더 및 채널 가져오기
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
    # Initialize an empty list to hold all messages
    all_messages = [] # 이렇게 할 경우 모듈화 불가

    if 'selected_channel' in st.session_state:
        try:
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

                            all_messages.extend(data) # Assuming each file contains a list of messages

                # st.write("success!")
                # st.write(fileNameList)
            else:
                st.error("선택한 채널의 데이터 파일이 존재하지 않습니다.")
        

            # 2. Data 가공_All_Message 
            # 2-1. 결측치 데이터 확인
            # Create a DataFrame from the messages
            df = pd.DataFrame(all_messages)

            # 2-2. 결측치 데이터 제거
            # Filter out rows with missing 'ts'
            df = df.dropna(subset=['ts'])

            # 2-3. Datatime 형식 변환
            from datetime import datetime

            # Convert timestamp to datetime and extract date
            df['date'] = df['ts'].apply(lambda x: datetime.fromtimestamp(float(x)).strftime('%y/%m/%d'))
            
            # 3. 일별 메시지 수치화
            # 3-1. 일별 메시지 계산
            # Group by date and count messages
            message_count = df['date'].value_counts().sort_index()

            # Convert the result to a DataFrame
            message_count_df = message_count.reset_index()
            message_count_df.columns = ['Date', 'Message Count']

##############################################
            # Content / Row 1
            with st.container(border=True):
                # st.write("일별 데이터 전송량") 

                # 4. Data-Visualization with Chart
                # Plot the data using Plotly
                fig = px.bar(message_count_df, x='Date', y='Message Count',
                            labels={'Date': 'Date', 'Message Count': 'Number of Messages'},
                            title='일별 메시지 전송 현황')

                # Update x-axis to show labels at specific intervals
                fig.update_xaxes(
                    tickmode='array',
                    tickvals=message_count_df['Date'][::5],  # Show every 5th label
                    ticktext=message_count_df['Date'][::5].astype(str)  # Labels to show as strings
                )

                # Show the plot in Streamlit
                st.plotly_chart(fig)

        ##############################################
            # Content / Row 2
            col1, col2, col3 = st.columns(3)

            with col1:
                with st.container(border=True):
                    # st.write("최대 전송량")
                    # # 최대 Message Count 검출
                    # max_message_count = message_count_df['Message Count'].max()
                    # max_message_count_date = message_count_df.loc[message_count_df['Message Count'].idxmax()]

                    st.write("메시지 평균 전송량")
                    avg_message_count = message_count_df['Message Count'].mean()
                    st.write(round(avg_message_count, 0), "건")

            with col2:
                with st.container(border=True):
                    st.write("메시지 평균 응답 시간")

                    # Copy data
                    df2 = df
                    # Convert timestamp fields to datetime
                    df2['ts'] = pd.to_datetime(df2['ts'].astype(float), unit='s')
                    df2['thread_ts'] = pd.to_datetime(df2['thread_ts'].astype(float), unit='s', errors='coerce')

                    # Filter messages that are replies in a thread
                    replies_df2 = df2.dropna(subset=['thread_ts'])

                    # Sort replies by thread_ts and ts to get the second reply in each thread
                    sorted_replies = replies_df2.sort_values(by=['thread_ts', 'ts'])
                    second_replies = sorted_replies.groupby('thread_ts').nth(1).reset_index()

                    # Join first replies with their original messages
                    merged_df2 = pd.merge(second_replies, df2, left_on='thread_ts', right_on='ts', suffixes=('_reply', '_original'))

                    # Calculate response time in minutes, hour, day
                    merged_df2['response_minute'] = (merged_df2['ts_reply'] - merged_df2['ts_original']).dt.total_seconds() / 60.0  # in minutes
                    merged_df2['response_hour'] = merged_df2['response_minute'] / 60.0  # in hour
                    merged_df2['response_day'] = merged_df2['response_hour'] / 24.0  # in day

                    # Calculate average response time in minutes
                    avg_response_minute = merged_df2['response_minute'].mean()
                    avg_response_hour = avg_response_minute / 60.0 # in hour
                    avg_response_day = avg_response_hour / 24.0 # in day

                    st.write(round(avg_response_day, 2), "일")
            
            with col3:
                with st.container(border=True):
                    st.write("메시지 평균 처리 시간")

                    # Copy data
                    df3 = df
                    # Convert timestamp fields to datetime
                    if not pd.api.types.is_datetime64_any_dtype(df3['ts']):
                        df3['ts'] = pd.to_datetime(df3['ts'].astype(float), unit='s')
                    if not pd.api.types.is_datetime64_any_dtype(df3['thread_ts']):
                        df3['thread_ts'] = pd.to_datetime(df3['thread_ts'].astype(float), unit='s', errors='coerce')

                    # Filter messages that are replies in a thread
                    replies_df3 = df3.dropna(subset=['thread_ts'])

                    # Sort replies by thread_ts and ts to get the last reply in each thread
                    sorted_replies = replies_df3.sort_values(by=['thread_ts', 'ts'])
                    last_replies = sorted_replies.groupby('thread_ts').last().reset_index()

                    # Join first replies with their original messages
                    merged_df3 = pd.merge(last_replies, df3, left_on='thread_ts', right_on='ts', suffixes=('_reply', '_original'))

                    # Calculate process time in minutes, hour, day
                    merged_df3['process_minute'] = (merged_df3['ts_reply'] - merged_df3['ts_original']).dt.total_seconds() / 60.0  # in minutes
                    merged_df3['process_hour'] = merged_df3['process_minute'] / 60.0  # in hour
                    merged_df3['process_day'] = merged_df3['process_hour'] / 24.0  # in day

                    # Calculate average process time in minutes
                    avg_process_minute = merged_df3['process_minute'].mean()
                    avg_process_hour = avg_process_minute / 60.0 # in hour
                    avg_process_day = avg_process_hour / 24.0 # in day

                    st.write(round(avg_process_day, 2), "일")
            
            # Content / Row 3
            col4, col5 = st.columns(2)
            
            with col4:
                with st.container(border=True):
                    st.write("주요 키워드")
                
                    # Wordcloud 생성
                    text = " ".join(message['text'] for message in all_messages if 'text' in message)
                    
                    # 한글 깨짐 방지: font 설정
                    font_path = "../assets/fonts/NotoSansKR-Regular.ttf"  

                    # 불용어 처리
                    text = re.sub(r'<@[^>]+>', '', text) # 유니코드 제거: 꺽쇠 괄호 안의 텍스트
                    text = re.sub(r'\n+', ' ', text) # 연속된 개행 문자 제거
                    text = re.sub(r'&gt;', ' ', text) # &gt; 패턴 제거
                    text = re.sub(r'&lt;', ' ', text) # &lt; 패턴 제거

                    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white').generate(text)
                    
                    # Wordcloud 표시
                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    st.pyplot(plt)
            
            with col5:
                with st.container(border=True):
                    st.write("추가 예정")

        except Exception as e:
            st.error(f"데이터 처리 중 오류가 발생했습니다: {str(e)}")

    else:
        with st.container(border=True):
            st.write("📣 좌측에서 채널을 선택해주세요.")

if __name__ == "__main__":
    main()