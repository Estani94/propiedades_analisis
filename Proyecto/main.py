import runpy
import subprocess

print("Ejecutando scrapping.py...")
runpy.run_path("scrapping.py")

print("Ejecutando analisis_propiedades.py...")
runpy.run_path("analisis_propiedades.py")

print("Lanzando dashboard con streamlit...")
subprocess.run(["streamlit", "run", "dash4.py"])
