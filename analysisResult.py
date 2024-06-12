import streamlit as st
import pandas as pd

def main():
    st.title("Analysis Page")

    # 업로드된 데이터가 세션 상태에 있는지 확인
    if 'uploaded_data' in st.session_state:
        df = st.session_state['uploaded_data']
        st.dataframe(df)
    else:
        st.write("No data uploaded.")

if __name__ == "__main__":
    main()