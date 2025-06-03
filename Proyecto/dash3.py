import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Cargar CSV limpio
df = pd.read_csv("propiedades_limpias_tipo.csv")

# Conversiones y columnas nuevas
df['Ambientes'] = pd.to_numeric(df['Ambientes'], errors='coerce')
df['Baños'] = pd.to_numeric(df['Baños'], errors='coerce')
df['Precio por m2'] = df['Precio USD'] / df['M2 Totales']
df['Rango de precio'] = pd.qcut(df['Precio USD'], q=4, labels=['Muy bajo', 'Bajo', 'Medio', 'Alto'])
df['Rango de superficie'] = pd.qcut(df['M2 Totales'], q=4, labels=['Chico', 'Mediano', 'Grande', 'Muy grande'])
df['Densidad ambientes'] = df['Ambientes'] / df['M2 Totales']

# Agrupar por tipo y rango de precio
precio_stats = df.groupby(['Tipo', 'Rango de precio'], observed=True).agg(
    Cantidad=('Precio USD', 'count'),
    Promedio_precio=('Precio USD', 'mean'),
    Min_precio=('Precio USD', 'min'),
    Max_precio=('Precio USD', 'max')
).reset_index()

# Ordenar para mejor visualización
precio_stats = precio_stats.sort_values(by=['Rango de precio', 'Tipo'])

# Agrupar por tipo y rango de superficie
superficie_stats = df.groupby(['Tipo', 'Rango de superficie'], observed=True).agg(
    Cantidad=('M2 Totales', 'count'),
    Promedio_m2=('M2 Totales', 'mean'),
    Min_m2=('M2 Totales', 'min'),
    Max_m2=('M2 Totales', 'max')
).reset_index()

superficie_stats = superficie_stats.sort_values(by=['Rango de superficie', 'Tipo'])

st.title("Dashboard de Propiedades")

# Mostrar tablas ordenadas
st.subheader("Estadísticas por rango de precio y tipo")
st.dataframe(precio_stats)

st.subheader("Estadísticas por rango de superficie y tipo")
st.dataframe(superficie_stats)

# Función para gráfico horizontal agrupado con valores al final
def plot_grouped_barh(df_stats, rango_col, tipo_col, cantidad_col, title, xlabel):
    fig, ax = plt.subplots(figsize=(12, 8))

    tipos = df_stats[tipo_col].unique()
    rangos = df_stats[rango_col].cat.categories.tolist()

    bar_height = 0.1
    y_ticks = np.arange(len(rangos))
    offsets = np.linspace(-bar_height*len(tipos)/2, bar_height*len(tipos)/2, len(tipos))

    for i, tipo in enumerate(tipos):
        subset = df_stats[df_stats[tipo_col] == tipo]
        cantidades = []
        for r in rangos:
            valor = subset.loc[subset[rango_col] == r, cantidad_col]
            cantidades.append(valor.values[0] if not valor.empty else 0)

        y_positions = y_ticks + offsets[i]
        bars = ax.barh(y_positions, cantidades, height=bar_height, label=tipo)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + max(cantidades)*0.01, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', va='center', fontsize=9)

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(rangos)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.legend(title='Tipo')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    return fig

# Gráfico para rango de precio
fig_precio = plot_grouped_barh(precio_stats, 'Rango de precio', 'Tipo', 'Cantidad',
                               'Cantidad de propiedades por tipo y rango de precio',
                               'Cantidad de propiedades')
st.pyplot(fig_precio)

# Gráfico para rango de superficie
fig_superficie = plot_grouped_barh(superficie_stats, 'Rango de superficie', 'Tipo', 'Cantidad',
                                   'Cantidad de propiedades por tipo y rango de superficie',
                                   'Cantidad de propiedades')
st.pyplot(fig_superficie)
