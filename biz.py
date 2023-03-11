import easyocr
import streamlit as st
from io import StringIO

reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory


def ocr_reader(file_path):
    data_list=[]
    result = reader.readtext(file_path)
    for i in result:
        data_list.append(i[1])
    return data_list


def streamlit_UI():
    st.set_page_config(page_title="BizCardX", layout="wide", initial_sidebar_state="collapsed")

    # Title and header to be dispalyed
    colT1, colT2 = st.columns([3, 5])
    with colT2:
        title = st.title(' :blue[BizCardX]')

    colT1, colT2 = st.columns([3, 5])
    with colT1:
        uploaded_file = st.file_uploader("Browse")
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            data_list = ocr_reader(bytes_data)
            st.write(data_list)


# Main call to UI which leads to excution of entire program
maincall = streamlit_UI()

