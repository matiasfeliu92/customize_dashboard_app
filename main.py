import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
uploaded_file = st.file_uploader('Select your CSV or Excel file', type=['csv', 'xlsx'])

df = None
columns = None
df_limit = None

if uploaded_file is not None:
    print(uploaded_file.name)
    if 'csv' in uploaded_file.name:
        df = pd.read_csv(uploaded_file, encoding='latin-1')
    elif 'xlsx' in uploaded_file.name:
        df = pd.read_excel(uploaded_file)

container = st.container()
col1, col2 = st.columns(2)
col3 = st.columns(1)
if df is not None:
    with container:
        with col1:
            columns = st.multiselect('Select columns', df.columns)
        with col2:
            df_limit = st.slider("", 0, len(df))
        if len(columns) > 0:                                   
            df = df[[col for col in columns]]
        print(df_limit)
        if df_limit==0:
            st.dataframe(df.head(10), use_container_width=True)
        else:
            st.dataframe(df.head(df_limit), use_container_width=True)