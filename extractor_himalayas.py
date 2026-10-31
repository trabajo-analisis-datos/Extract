import requests
import pandas as pd
from datetime import datetime

def extraer_datos_crudos():
    url = "https://himalayas.app/jobs/api"
    print(f"Consultando la API: {url}")
    
    # 1. Obtener los datos crudos en formato JSON
    response = requests.get(url)
    response.raise_for_status() 
    datos_json = response.json()
    
    # Extraer la lista de ofertas contenida en el nodo 'jobs'
    ofertas = datos_json.get('jobs', [])
    
    # 2. Convertir a un DataFrame tabular y exportar a CSV sin limpiar
    df = pd.DataFrame(ofertas)
    
    # Generar un nombre de archivo con marca de tiempo
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    archivo_csv = f"himalayas_raw_{timestamp}.csv"
    
    # Exportar el archivo preservando todos los campos originales
    df.to_csv(archivo_csv, index=False, encoding='utf-8')
    print(f"Extracción exitosa: {len(df)} registros guardados intactos en '{archivo_csv}'")

if __name__ == "__main__":
    extraer_datos_crudos()