import pandas as pd

# Leer el CSV
df = pd.read_csv("propiedades_bruto.csv")

# Filtrar precios no válidos
df = df[~df['Precio USD'].astype(str).str.contains('ARS|Solicitar', na=False)]

# Eliminar puntos y comas, convertir a número
df['Precio USD'] = df['Precio USD'].astype(str).str.replace('.', '', regex=False)
df['Precio USD'] = pd.to_numeric(df['Precio USD'], errors='coerce')

# Limpiar y convertir m2
df['M2 Totales'] = df['M2 Totales'].astype(str).str.replace(',', '.', regex=False)
df['M2 Totales'] = pd.to_numeric(df['M2 Totales'], errors='coerce')

# Eliminar filas con valores faltantes
df = df.dropna(subset=['Precio USD', 'M2 Totales'])

# Eliminar duplicados
df = df.drop_duplicates(subset=['Dirección', 'Precio USD', 'M2 Totales'])

# Mapear patrones por tipo incluyendo sinónimos y abreviaturas
tipos = {
    'Departamento': r'\b(departamento|dpto|dto|dept|depto)\b',
    'Casa': r'\bcasa\b',
    'Terreno': r'\bterreno\b',
    'Salón': r'\bsal[oó]n\b',
    'Galpón': r'\bgalp[oó]n\b',
    'Cochera': r'\bcochera\b',
    'Local': r'\blocal\b',
    'Oficina': r'\boficina\b',
    'PH': r'\bPH\b',
    'Campo': r'\bcampo\b',
    'Quinta': r'\bquinta\b'
}

def detectar_tipo(nombre):
    nombre = str(nombre).lower()
    for tipo, patron in tipos.items():
        if pd.notna(nombre) and pd.Series(nombre).str.contains(patron, regex=True).any():
            return tipo
    return "Otro"

df['Tipo'] = df['Nombre'].apply(detectar_tipo)

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

df.to_csv("propiedades_limpias_tipo.csv", index=False, encoding='utf-8')