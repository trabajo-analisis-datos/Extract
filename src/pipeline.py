from datetime import datetime

# Importamos los submódulos que acabamos de crear
from extractor import extraer_ofertas_himalayas
from transformador import filtrar_solo_tecnologia, estandarizar_estructura_json
from persistencia import guardar_ofertas_json

def ejecutar_pipeline():
    print("[PIPELINE] INICIANDO ORQUESTACIÓN DE DATOS...")
    
    # 1. Definir la fecha objetivo (hoy)
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    # 2. Fase de EXTRACCIÓN
    # Trae los datos de la API a la memoria
    datos_crudos = extraer_ofertas_himalayas(fecha_hoy, limite_maximo=1000)
    
    if not datos_crudos:
        print("[PIPELINE] Abortando: No se extrajeron datos crudos.")
        return

    # 3. Fase de TRANSFORMACIÓN
    # Pasamos los datos crudos por el filtro de tecnología
    datos_ti = filtrar_solo_tecnologia(datos_crudos)
    
    # Estandarizamos las llaves (Modelo de dominio con nulos)
    datos_estandarizados = estandarizar_estructura_json(datos_ti)
    
    # 4. Fase de PERSISTENCIA
    # Guardamos el resultado final en la carpeta /data
    guardar_ofertas_json(datos_estandarizados, fecha_hoy)
    
    print("[PIPELINE] EJECUCIÓN COMPLETADA CON ÉXITO.")

if __name__ == "__main__":
    ejecutar_pipeline()