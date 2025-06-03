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

# Agrupar por Tipo y rango de precio
precio_stats = df.groupby(['Tipo', 'Rango de precio'], observed=True).agg(
    Cantidad=('Precio USD', 'count'),
    Promedio_precio=('Precio USD', 'mean'),
    Min_precio=('Precio USD', 'min'),
    Max_precio=('Precio USD', 'max')
).reset_index()

# Agrupar por Tipo y rango de superficie
superficie_stats = df.groupby(['Tipo', 'Rango de superficie'], observed=True).agg(
    Cantidad=('M2 Totales', 'count'),
    Promedio_m2=('M2 Totales', 'mean'),
    Min_m2=('M2 Totales', 'min'),
    Max_m2=('M2 Totales', 'max')
).reset_index()

st.title("Dashboard Propiedades")

st.subheader("Estadísticas por tipo y rango de precio")
st.dataframe(precio_stats)

# Gráfico cantidad por rango de precio y tipo
fig, ax = plt.subplots(figsize=(10, 6))
tipos = precio_stats['Tipo'].unique()
colores = plt.cm.tab10.colors  # hasta 10 colores distintos

for i, tipo in enumerate(tipos):
    subset = precio_stats[precio_stats['Tipo'] == tipo]
    ax.bar(subset['Rango de precio'], subset['Cantidad'], label=tipo, color=colores[i % 10], alpha=0.7)

ax.set_xlabel('Rango de precio')
ax.set_ylabel('Cantidad de propiedades')
ax.set_title('Cantidad de propiedades por rango de precio y tipo')
ax.legend(title='Tipo')
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Estadísticas por tipo y rango de superficie")
st.dataframe(superficie_stats)

# Gráfico cantidad por rango de superficie y tipo
fig2, ax2 = plt.subplots(figsize=(10, 6))
tipos2 = superficie_stats['Tipo'].unique()

for i, tipo in enumerate(tipos2):
    subset = superficie_stats[superficie_stats['Tipo'] == tipo]
    ax2.bar(subset['Rango de superficie'], subset['Cantidad'], label=tipo, color=colores[i % 10], alpha=0.7)

ax2.set_xlabel('Rango de superficie')
ax2.set_ylabel('Cantidad de propiedades')
ax2.set_title('Cantidad de propiedades por rango de superficie y tipo')
ax2.legend(title='Tipo')
plt.xticks(rotation=45)
st.pyplot(fig2)