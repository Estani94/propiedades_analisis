import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Cargar el CSV limpio
df = pd.read_csv("propiedades_limpias_tipo.csv")

# Asegurar conversiones numéricas
df['Ambientes'] = pd.to_numeric(df['Ambientes'], errors='coerce')
df['Baños'] = pd.to_numeric(df['Baños'], errors='coerce')

# 1. Precio por m²
df['Precio por m2'] = df['Precio USD'] / df['M2 Totales']

# 4. Rango de precio por cuartiles
df['Rango de precio'] = pd.qcut(df['Precio USD'], q=4, labels=['Muy bajo', 'Bajo', 'Medio', 'Alto'])

# 5. Rango de superficie por cuartiles
df['Rango de superficie'] = pd.qcut(df['M2 Totales'], q=4, labels=['Chico', 'Mediano', 'Grande', 'Muy grande'])

# 6. Densidad de ambientes
df['Densidad ambientes'] = df['Ambientes'] / df['M2 Totales']

# Agrupar por rango de precio
precio_stats = df.groupby('Rango de precio', observed=True).agg(
    Cantidad=('Precio USD', 'count'),
    Promedio_precio=('Precio USD', 'mean'),
    Min_precio=('Precio USD', 'min'),
    Max_precio=('Precio USD', 'max')
).reset_index()

# Agrupar por rango de superficie
superficie_stats = df.groupby('Rango de superficie').agg(
    Cantidad=('M2 Totales', 'count'),
    Promedio_m2=('M2 Totales', 'mean'),
    Min_m2=('M2 Totales', 'min'),
    Max_m2=('M2 Totales', 'max')
).reset_index()

st.title("Dashboard Propiedades")

st.subheader("Estadísticas por rango de precio")
st.dataframe(precio_stats)

fig, ax = plt.subplots()
ax.bar(precio_stats['Rango de precio'], precio_stats['Cantidad'])
ax.set_xlabel('Rango de precio')
ax.set_ylabel('Cantidad de propiedades')
ax.set_title('Cantidad de propiedades por rango de precio')
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Estadísticas por rango de superficie")
st.dataframe(superficie_stats)

fig2, ax2 = plt.subplots()
ax2.bar(superficie_stats['Rango de superficie'], superficie_stats['Cantidad'])
ax2.set_xlabel('Rango de superficie')
ax2.set_ylabel('Cantidad de propiedades')
ax2.set_title('Cantidad de propiedades por rango de superficie')
plt.xticks(rotation=45)
st.pyplot(fig2)