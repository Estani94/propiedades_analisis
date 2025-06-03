# 🏡 Análisis de Propiedades en Argentina

Este proyecto realiza un análisis exploratorio de datos (EDA) sobre propiedades inmobiliarias en Argentina, utilizando Python y Streamlit para crear una aplicación web interactiva. La aplicación permite visualizar y explorar datos relacionados con precios, ubicaciones y características de las propiedades.

## 📁 Estructura del Proyecto

```
propiedades_analisis/
├── Proyecto/
│   ├── analisis_propiedades.py
│   ├── dash4.py
│   ├── main.py
│   ├── scrapping.py
│   ├── propiedades_bruto.csv
│   ├── propiedades_limpias_tipo.csv
│   └── requirements.txt
```

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Estani94/propiedades_analisis.git
   cd propiedades_analisis/Proyecto
   ```

2. **Crear un entorno virtual (opcional pero recomendado):**

   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación Streamlit:**

   ```bash
   streamlit run dash4.py
   ```

   > **Nota:** Asegúrate de que los archivos `propiedades_limpias_tipo.csv` y `dash4.py` estén en el mismo directorio. Si estás utilizando Streamlit Cloud, verifica que el archivo CSV esté en la misma carpeta que el script principal o ajusta la ruta en el código según sea necesario.

## 🧰 Tecnologías Utilizadas

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [Pandas](https://pandas.pydata.org/)
* [Matplotlib](https://matplotlib.org/)
* [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium)

## 📊 Funcionalidades

* Visualización interactiva de datos de propiedades.
* Gráficos de distribución de precios y características.
* Filtros y opciones para explorar diferentes tipos de propiedades.

## ⚠️ Posibles Errores y Soluciones

* **FileNotFoundError:** Si al ejecutar la aplicación aparece un error indicando que no se encuentra el archivo `propiedades_limpias_tipo.csv`, verifica que el archivo esté en el mismo directorio que `dash4.py`. Si estás utilizando Streamlit Cloud, asegúrate de que el archivo CSV esté en la misma carpeta que el script principal o ajusta la ruta en el código según sea necesario.

* **ModuleNotFoundError:** Si falta alguna biblioteca, asegúrate de haber instalado todas las dependencias listadas en `requirements.txt`.
