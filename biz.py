import easyocr
import pandas as pd
import streamlit as st

reader = easyocr.Reader(['ch_sim', 'en'])  # this needs to run only once to load the model into memory


def ocr_reader(file_path):
    data_list = []
    result = reader.readtext(file_path)
    for i in result:
        data_list.append(i[1])
    return data_list


def analyze_txt(data_list):
    final_data = {}
    addstr = ""
    phonestr = ""
    cn = ""
    for i in range(len(data_list)):
        if i == 0:
            final_data['Name'] = data_list[i]
            continue
        if i == 1:
            final_data['Designation'] = data_list[i]
            continue
        if "-" in data_list[i]:
            phonestr = " , ".join([phonestr, data_list[i]])
            final_data['Phone Number'] = phonestr[2:]
            continue
        if "@" in data_list[i]:
            final_data['Email'] = data_list[i]
            continue
        if "WWW" in data_list[i] or "www" in data_list[i] or "TTT" in data_list[i] or ".com" in data_list[i]:
            if "@" not in data_list[i]:
                final_data['Website'] = data_list[i]
            continue
        if "-" not in data_list[i] and "@" not in data_list[i] and "www" not in data_list[i] and "WWW" not in data_list[
            i]:
            if any(char.isdigit() for char in data_list[i]) or "," in data_list[i] or ";" in data_list[i]:
                addstr = addstr + data_list[i]
                final_data['Address'] = addstr
                continue
            else:
                cn = " ".join([cn, data_list[i]])
                final_data['Company Name'] = cn[0:]
                continue

    return final_data


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
            final_data = analyze_txt(data_list)
            st.table(pd.DataFrame.from_dict(final_data, orient='index'))
    with colT2:
        st.image(bytes_data, caption='Buisness Card')


# Main call to UI which leads to excution of entire program
maincall = streamlit_UI()
