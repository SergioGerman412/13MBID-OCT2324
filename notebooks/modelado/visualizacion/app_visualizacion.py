import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Se realiza la lectura de los datos
df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

# Título del dashboard
st.write("# 13MBID - Visualización de datos")
st.write("## Panel de visualización generado sobre los datos de créditos y tarjetas emitidas a clientes de la entidad")
st.write("#### Persona/s: Sergio German Quispe - Gianmarcos Espinoza Pachas")
st.write("----")

# Gráficos
st.write("### Caracterización de los créditos otorgados")

# Se tienen que agregar las definiciones de gráficos desde la libreta
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Se realiza la "impresión" del gráfico en el dashboard
st.plotly_chart(creditos_x_objetivo)


# Histograma de los importes de créditos otorgados
histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')

st.plotly_chart(histograma_importes)

# Filtros

option = st.selectbox(
    'Qué tipo de crédito desea filtrar?',
     df['objetivo_credito'].unique())

df_filtrado = df[df['objetivo_credito'] == option]

st.write(f"Tipo de crédito seleccionado: {option}")

if st.checkbox('Mostrar créditos finalizados?', value=True):

    # Conteo de ocurrencias por estado
    estado_credito_counts = df_filtrado['estado_credito_N'].value_counts()

    # Gráfico de torta de estos valores
    fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
    fig.update_layout(title_text='Distribución de créditos por estado registrado')
else:
    df_filtrado = df_filtrado[df_filtrado['estado_credito_N'] == 'P']
    # Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()

    # Create a Pie chart
    fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig.update_layout(title_text='Distribución de créditos en función de registro de mora')

st.write(f"Cantidad de créditos con estas condiciones: {df_filtrado.shape[0]}")
st.plotly_chart(fig)


#gráfica  Comparación de genero y falta de pago (gráfico de barras apiladas)


status_vs_default = pd.crosstab(df['genero'], df['falta_pago'])
fig, ax = plt.subplots(figsize=(8, 6))
status_vs_default.plot(kind='bar', stacked=True, color=['green', 'red'], ax=ax)
plt.title('Comparación de género y falta de pago')
plt.xlabel('Género')
plt.ylabel('Número de préstamos')
plt.xticks(rotation=45)
plt.legend(title='Falta de Pago', labels=['No', 'Sí'])

# Mostrar el gráfico con Streamlit
st.pyplot(fig)


#Gráfica relación entre el objetivo de crédito y falta de pago

custom_colors = {'N': 'green', 'Y': 'red'}

plt.figure(figsize=(10, 6))
ax = sns.countplot(x='objetivo_credito', hue='falta_pago', data=df, palette=custom_colors)

# Agregar conteo redondeado en la parte superior de cada barra
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{round(height)}', (p.get_x() + p.get_width() / 2., height), ha='center', va='bottom', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

plt.title('Relación entre el objetivo del crédito y la falta de pago')
plt.xlabel('Objetivo del crédito')
plt.ylabel('Número de préstamos')
plt.xticks(rotation=45)
plt.legend(title='Falta de Pago', labels=['No', 'Sí'])

st.pyplot(plt)

#Gráfica de distribución de niveles educativos de los clientes

def plot_niveles_educativos(df):
    # Obtener el conteo de cada nivel educativo
    conteo_nivel_educativo = df['nivel_educativo'].value_counts()

    # Crear el gráfico de barras de la distribución de niveles educativos
    fig, ax = plt.subplots(figsize=(8, 6))
    grafico = conteo_nivel_educativo.plot(kind='bar', color='skyblue', ax=ax)

    # Agregar el conteo encima de cada barra
    for indice, valor in enumerate(conteo_nivel_educativo):
        ax.text(indice, valor + 0.1, str(valor), ha='center', va='bottom')

    plt.title('Distribución de Niveles Educativos de los Clientes')
    plt.xlabel('Nivel Educativo')
    plt.ylabel('Número de Clientes')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

# Llamar a la función con el dataframe 'df'
plot_niveles_educativos(df)