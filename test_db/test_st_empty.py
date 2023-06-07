import streamlit as st
import time


with st.empty():
    with st.container():
        st.write('1')
        time.sleep(3)
    with st.container():
        st.write('2')
        time.sleep(3)
    with st.container():
        st.write('3')
        time.sleep(3)