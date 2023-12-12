import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
uploaded_file = st.file_uploader('Select your CSV or Excel file', type=['csv', 'xlsx'])

df: pd.DataFrame() = None
columns = None
df_limit = None
select_value = None
set_groupby = None
selected_values = []
selected_groupby = []
fig = None

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
    st.write(f'The data has {df.shape[0]} rows and {df.shape[1]} columns')
    st.dataframe(df.describe(), use_container_width=True)
    st.header('Filters')
    set_filters = st.checkbox('Set filters')
    if set_filters:
        columns = st.columns(2)
        for i, col in enumerate(df.columns):
            select_value = columns[i % 2].multiselect(f'Select options for {col}', df[col].unique(), key=f'option_{i}')
            selected_values.extend(select_value)
            # FALTA AGREGAR MODIFICACIONES DEL DATAFRAME CON LOS VALORES SELECCIONADOS
    st.header('GroupBy')
    set_groupby = st.checkbox('Set groupby')
    if set_groupby:
        select_group_by = st.multiselect('Select option for groupby', df.columns)
        selected_groupby.extend(select_group_by)
        # FALTA AGREGAR MODIFICACIONES DEL DATAFRAME CON LOS VALORES SELECCIONADOS

    st.header('Graphics')
    graphs_types = ['histogram', 'boxplot', 'line', 'pie', 'bar', 'barh']
    select_graph = st.selectbox('Select one graph type', graphs_types)

    if select_graph == 'histogram':
        # fig = px.histogram(df.select_dtypes(include='number'))
        fig = px.histogram(df.select_dtypes(include='number'), x=df.select_dtypes(include='number'), marginal="box")
        fig.update_layout(
            width=10*80,
            height=8*80,
        )
        st.plotly_chart(fig)