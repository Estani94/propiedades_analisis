import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("propiedades_limpias_tipo.csv")

# Conversiones necesarias
df['Precio USD'] = pd.to_numeric(df['Precio USD'], errors='coerce')
df['M2 Totales'] = pd.to_numeric(df['M2 Totales'], errors='coerce')
df['Ambientes'] = pd.to_numeric(df['Ambientes'], errors='coerce')
df['Baños'] = pd.to_numeric(df['Baños'], errors='coerce')

# Crear columnas calculadas si no existen
if 'Precio por m2' not in df.columns:
    df['Precio por m2'] = df['Precio USD'] / df['M2 Totales']
if 'Densidad ambientes' not in df.columns:
    df['Densidad ambientes'] = df['Ambientes'] / df['M2 Totales']

# Definir rangos por cuartiles si no existen
if 'Rango de precio' not in df.columns:
    df['Rango de precio'] = pd.qcut(df['Precio USD'], q=4, labels=['Muy bajo', 'Bajo', 'Medio', 'Alto'])
if 'Rango de superficie' not in df.columns:
    df['Rango de superficie'] = pd.qcut(df['M2 Totales'], q=4, labels=['Chico', 'Mediano', 'Grande', 'Muy grande'])

st.title("Dashboard Maestro de Propiedades")

# --- FILTROS ---
st.sidebar.header("Filtros")
tipos_disponibles = sorted(df['Tipo'].dropna().unique())
tipo_seleccionado = st.sidebar.multiselect("Tipo de propiedad", tipos_disponibles, default=tipos_disponibles)

precio_min = int(df['Precio USD'].min())
precio_max = int(df['Precio USD'].max())
precio_rango = st.sidebar.slider("Rango de precio USD", precio_min, precio_max, (precio_min, precio_max))

superficie_min = int(df['M2 Totales'].min())
superficie_max = int(df['M2 Totales'].max())
superficie_rango = st.sidebar.slider("Rango de superficie (m2)", superficie_min, superficie_max, (superficie_min, superficie_max))

ambientes_min = int(df['Ambientes'].min())
ambientes_max = int(df['Ambientes'].max())
ambientes_rango = st.sidebar.slider("Cantidad de ambientes", ambientes_min, ambientes_max, (ambientes_min, ambientes_max))

banos_min = int(df['Baños'].min())
banos_max = int(df['Baños'].max())
banos_rango = st.sidebar.slider("Cantidad de baños", banos_min, banos_max, (banos_min, banos_max))

# Filtrar el dataframe
df_filtrado = df[
    (df['Tipo'].isin(tipo_seleccionado)) &
    (df['Precio USD'] >= precio_rango[0]) & (df['Precio USD'] <= precio_rango[1]) &
    (df['M2 Totales'] >= superficie_rango[0]) & (df['M2 Totales'] <= superficie_rango[1]) &
    (df['Ambientes'] >= ambientes_rango[0]) & (df['Ambientes'] <= ambientes_rango[1]) &
    (df['Baños'] >= banos_rango[0]) & (df['Baños'] <= banos_rango[1])
]

st.markdown(f"**Propiedades seleccionadas: {len(df_filtrado)}**")

# --- MÉTRICAS ---
st.header("Métricas generales")

col1, col2, col3 = st.columns(3)
col1.metric("Precio USD promedio", f"${df_filtrado['Precio USD'].mean():,.0f}")
col2.metric("Superficie promedio (m²)", f"{df_filtrado['M2 Totales'].mean():.1f}")
col3.metric("Ambientes promedio", f"{df_filtrado['Ambientes'].mean():.1f}")

col4, col5 = st.columns(2)
col4.metric("Precio promedio por m²", f"${df_filtrado['Precio por m2'].mean():,.0f}")
col5.metric("Densidad ambientes (amb/m²)", f"{df_filtrado['Densidad ambientes'].mean():.3f}")

# --- TABLAS DE ESTADÍSTICAS ---

st.header("Estadísticas por rango de precio y tipo")

stats_precio = df_filtrado.groupby(['Tipo', 'Rango de precio'], observed=True).agg(
    Cantidad=('Precio USD', 'count'),
    Promedio_precio=('Precio USD', 'mean'),
    Min_precio=('Precio USD', 'min'),
    Max_precio=('Precio USD', 'max')
).reset_index().sort_values(['Tipo', 'Rango de precio'])

st.dataframe(stats_precio.style.format({
    'Promedio_precio': "${:,.0f}",
    'Min_precio': "${:,.0f}",
    'Max_precio': "${:,.0f}"
}))

st.header("Estadísticas por rango de superficie y tipo")

stats_superficie = df_filtrado.groupby(['Tipo', 'Rango de superficie'], observed=True).agg(
    Cantidad=('M2 Totales', 'count'),
    Promedio_m2=('M2 Totales', 'mean'),
    Min_m2=('M2 Totales', 'min'),
    Max_m2=('M2 Totales', 'max')
).reset_index().sort_values(['Tipo', 'Rango de superficie'])

st.dataframe(stats_superficie.style.format({
    'Promedio_m2': "{:.1f}",
    'Min_m2': "{:.1f}",
    'Max_m2': "{:.1f}"
}))

# --- GRÁFICOS ---

# Barra horizontal con cantidad por rango de precio y tipo
st.header("Cantidad de propiedades por rango de precio y tipo")
fig, ax = plt.subplots(figsize=(10,6))

for tipo in tipo_seleccionado:
    subset = stats_precio[stats_precio['Tipo'] == tipo]
    ax.barh(subset['Rango de precio'].astype(str) + " (" + tipo + ")", subset['Cantidad'], label=tipo)

for i, v in enumerate(stats_precio['Cantidad']):
    ax.text(v + 1, i, str(v), va='center')

ax.set_xlabel("Cantidad de propiedades")
ax.set_ylabel("Rango de precio")
ax.legend(title="Tipo")
st.pyplot(fig)

# Barra horizontal con cantidad por rango de superficie y tipo
st.header("Cantidad de propiedades por rango de superficie y tipo")
fig2, ax2 = plt.subplots(figsize=(10,6))

for tipo in tipo_seleccionado:
    subset = stats_superficie[stats_superficie['Tipo'] == tipo]
    ax2.barh(subset['Rango de superficie'].astype(str) + " (" + tipo + ")", subset['Cantidad'], label=tipo)

for i, v in enumerate(stats_superficie['Cantidad']):
    ax2.text(v + 1, i, str(v), va='center')

ax2.set_xlabel("Cantidad de propiedades")
ax2.set_ylabel("Rango de superficie")
ax2.legend(title="Tipo")
st.pyplot(fig2)

# Boxplot Precio por m²
st.header("Distribución del Precio por m² por Tipo")
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.boxplot(data=df_filtrado, x='Tipo', y='Precio por m2', ax=ax3)
ax3.set_yscale('log')
ax3.set_ylabel("Precio por m² (escala logarítmica)")
ax3.set_xlabel("Tipo de propiedad")
st.pyplot(fig3)

# Histogramas para Ambientes y Densidad
st.header("Distribución de Ambientes")
fig4, ax4 = plt.subplots(figsize=(10,4))
sns.histplot(df_filtrado, x='Ambientes', bins=20, kde=False, hue='Tipo', multiple='stack', ax=ax4)
st.pyplot(fig4)

st.header("Distribución de Densidad de Ambientes (ambientes/m²)")
fig5, ax5 = plt.subplots(figsize=(10,4))
sns.histplot(df_filtrado, x='Densidad ambientes', bins=30, kde=True, hue='Tipo', multiple='stack', ax=ax5)
st.pyplot(fig5)

# Mostrar tabla con propiedades filtradas
st.header("Listado de propiedades filtradas")
st.dataframe(df_filtrado.sort_values(by='Precio USD'))