import streamlit as st
import pages.home as home
import pages.analysisResult as analysisResult

# 페이지를 세션 상태에서 관리
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# 페이지 전환 로직
if st.session_state['page'] == 'home':
    home.main()
elif st.session_state['page'] == 'analysisResult':
    analysisResult.main()
