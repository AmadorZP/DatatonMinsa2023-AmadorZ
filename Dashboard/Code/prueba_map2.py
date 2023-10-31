import streamlit as st
import pydeck as pdk
import pandas as pd

# Carga tu dataframe aquí
df_CANCER_ATENDIDOS_SAMPLE = pd.read_csv('C:\Dataton_2023\DATATON - MINSA 2023\Cancer dataton\Maps\df_CANCER_ATENDIDOS_TIPOS.csv')
df_CANCER_ATENDIDOS_SAMPLE.drop(['Unnamed: 0'], axis=1, inplace=True)
df_CANCER_ATENDIDOS_SAMPLE['COORDINATES'] = df_CANCER_ATENDIDOS_SAMPLE[['longitud', 'latitud']].apply(tuple, axis=1)

st.title('Visualización de datos sobre el cáncer en Perú')

# Dropdown para seleccionar el tipo de cáncer
tipo_cancer = st.selectbox('Elige un tipo de cáncer:', ['Todos'] + list(df_CANCER_ATENDIDOS_SAMPLE['Tipos de cáncer'].unique()))
if tipo_cancer != 'Todos':
    df_CANCER_ATENDIDOS_SAMPLE = df_CANCER_ATENDIDOS_SAMPLE[df_CANCER_ATENDIDOS_SAMPLE['Tipos de cáncer'] == tipo_cancer]

# Dropdown para seleccionar el año
year = st.selectbox('Elige un año:', ['Todos'] + sorted(list(df_CANCER_ATENDIDOS_SAMPLE['Year'].unique())))
if year != 'Todos':
    df_CANCER_ATENDIDOS_SAMPLE = df_CANCER_ATENDIDOS_SAMPLE[df_CANCER_ATENDIDOS_SAMPLE['Year'] == int(year)]

# Dropdown para seleccionar el sexo
sexo = st.selectbox('Elige un sexo:', ['Todos'] + list(df_CANCER_ATENDIDOS_SAMPLE['Sexo'].unique()))
if sexo != 'Todos':
    df_CANCER_ATENDIDOS_SAMPLE = df_CANCER_ATENDIDOS_SAMPLE[df_CANCER_ATENDIDOS_SAMPLE['Sexo'] == sexo]

# Sliders para seleccionar un intervalo de edad
min_edad, max_edad = st.slider('Elige un rango de edad:', int(df_CANCER_ATENDIDOS_SAMPLE['Edad'].min()), int(df_CANCER_ATENDIDOS_SAMPLE['Edad'].max()), (int(df_CANCER_ATENDIDOS_SAMPLE['Edad'].min()), int(df_CANCER_ATENDIDOS_SAMPLE['Edad'].max())))
df_CANCER_ATENDIDOS_SAMPLE = df_CANCER_ATENDIDOS_SAMPLE[(df_CANCER_ATENDIDOS_SAMPLE['Edad'] >= min_edad) & (df_CANCER_ATENDIDOS_SAMPLE['Edad'] <= max_edad)]

# Dropdown para seleccionar el departamento
departamento = st.selectbox('Elige un departamento:', ['Todos'] + list(df_CANCER_ATENDIDOS_SAMPLE['departamento'].unique()))
if departamento != 'Todos':
    df_CANCER_ATENDIDOS_SAMPLE = df_CANCER_ATENDIDOS_SAMPLE[df_CANCER_ATENDIDOS_SAMPLE['departamento'] == departamento]

# Crear y mostrar el mapa
layer = pdk.Layer(
    "HexagonLayer",
    df_CANCER_ATENDIDOS_SAMPLE,
    auto_highlight=True,
    pickable=True,
    extruded=True,
    cell_size=10000,  
    elevation_scale=100,
    get_position="COORDINATES",
    get_fill_color="[255, (1-elevationValue) * 255, 255]",

)
view_state = pdk.ViewState(latitude=-11.4839, longitude=-76.1333, zoom=6, bearing=0.36, pitch=50)
r = pdk.Deck(layers=[layer],
              initial_view_state=view_state,
        tooltip={
        'html': '<b>Número de pacientes: </b>{elevationValue}',
        'style': {
            'backgroundColor': 'steelblue',
            'color': 'white'
        }
    })
st.pydeck_chart(r)
