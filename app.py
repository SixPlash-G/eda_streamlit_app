import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Titulo principal
st.title("Analisis Exploratorio de Datos")

#leer el archivo Excel
data=pd.read_csv(r"C:\Users\jaiso\Desktop\Proyecto Mineria\STREAMLIT\knime_result_datos_nuevos.csv", encoding='latin1')
st.success("Archivo cargado con exito")

st.write(data.head())

st.write("Dimenciones de los datos")
st.write(f"Fila: {data.shape[0]}, Columnas: {data.shape[1]}")


#Estadisticas descriptivas
st.header("Estadisticas descriptivas")
st.write(data.describe(include='all'))

#Tablas dinamicas
st.header("Tablas dinamicas")
col1, col2 = st.columns(2)
with col1:
    row_variable=st.selectbox("variable para filas", options=data.columns, key="rows")
with col2:
    col_variable=st.selectbox("variable para columna", options=data.columns, key="cols")

if row_variable and col_variable:
    pivot_table=data.pivot_table(index=row_variable, columns=col_variable, aggfunc="size", fill_value=0)
    st.write("Tabla dinamica")
    st.dataframe(pivot_table)

#Graficos cualitativos y cuantitativos
st.header("Graficos")

st.subheader("Graficos de distribucion")
numeric_columns=data.select_dtypes(include=["number"]).columns
categorical_columns=data.select_dtypes(include=["object", "category"]).columns

if numeric_columns.any():
    column_top_plot=st.selectbox("Selecciona una columna numerica", options=numeric_columns, key="num_col")
    plt.figure(figsize=(10, 5))
    sns.histplot(data[column_top_plot], kde=True, color="blue")
    plt.title(f"Distribucion de {column_top_plot}")
    st.pyplot(plt)

if categorical_columns.any():
    column_top_plot=st.selectbox("Selecciona una columna categorica", options=categorical_columns, key="cat_col")
    plt.figure(figsize=(10, 5))
    sns.countplot(data[column_top_plot], palette="viridis")
    plt.title(f"Conteo de {column_top_plot}")
    st.pyplot(plt)   

st.subheader("Matriz de correlacion")
if numeric_columns.any():
    corr_matrix=data[numeric_columns].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de correlacion")
    st.pyplot(plt)


st.header("Filtros dinamicos")
st.write("Selecciona columnas para aplicar filtros:")
selected_columns=st.multiselect("selecciona columnas", options=data.columns)

if selected_columns:
    filters={}
    for column in selected_columns:
        if data[column].dtype == 'object':
            filters[column]=st.multiselect(f"Filtrar {column}", options=data[column].unique())
        else:
            min_val=data[column].min()
            max_val=data[column].max()
            filters[column]=st.slider(f"Filtrar {column}", min_val, max_val, (min_val, max_val))
    filtered_data=data.copy()
    for column, filter_value in filters.items():
        if isinstance(filter_value, list):
            filtered_data=filtered_data[filtered_data[column].isin(filter_value)]
        else:
            filtered_data=filtered_data[(filtered_data[column]>=filter_value[0]) & (filtered_data[column]<=filter_value[1])]
    st.write("Datos filtrados")
    st.dataframe(filtered_data)

#Resumen final
st.header("Resumen final")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Numero de filas", data.shape[0])
        st.metric("Numero de columnas", data.shape[1])
    with col2:
        st.metric("Valores nulos", data.isnull().sum().sum())
        st.metric("Campos unicos", data.nunique().sum())