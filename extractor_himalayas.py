import requests
import pandas as pd
from datetime import datetime
import time

def extraer_ofertas_por_dia(fecha_objetivo_str):
    url = "https://himalayas.app/jobs/api"
    ofertas_del_dia = []
    
    limit = 20
    cursor = None
    continuar_buscando = True
    
    # Configuración para reintentos por fallos de conexión (SSLError)
    max_reintentos = 3
    
    print(f"Iniciando extracción masiva para el día: {fecha_objetivo_str}")
    fecha_objetivo = datetime.strptime(fecha_objetivo_str, "%Y-%m-%d").date()
    
    while continuar_buscando:
        print(f"Consultando API... (Cursor: {cursor})")
        
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
            
        intentos_fallidos = 0
        peticion_exitosa = False
        
        # Bucle interno de reintentos
        while intentos_fallidos < max_reintentos and not peticion_exitosa:
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status() 
                datos_json = response.json()
                peticion_exitosa = True
                
            except requests.exceptions.RequestException as e:
                intentos_fallidos += 1
                print(f"Error de conexión (Intento {intentos_fallidos}/{max_reintentos}): {e}")
                if intentos_fallidos < max_reintentos:
                    print("Esperando 5 segundos antes de reintentar...")
                    time.sleep(5)
                else:
                    print("Máximo de reintentos alcanzado. Abortando extracción en este point.")
                    # Rompemos el ciclo principal, pero NO borramos ofertas_del_dia
                    continuar_buscando = False 
        
        if not peticion_exitosa:
            break
            
        ofertas_pagina = datos_json.get('jobs', [])
        
        if not ofertas_pagina:
            print("No hay más ofertas en la plataforma.")
            break
            
        for oferta in ofertas_pagina:
            fecha_timestamp = oferta.get('pubDate')
            
            if fecha_timestamp:
                fecha_oferta = datetime.fromtimestamp(fecha_timestamp).date()
                
                if fecha_oferta == fecha_objetivo:
                    ofertas_del_dia.append(oferta)
                    
                elif fecha_oferta < fecha_objetivo:
                    print(f"Se alcanzó el día {fecha_oferta}. Deteniendo extracción.")
                    continuar_buscando = False
                    break
        
        # Continuar si todo salió bien
        if continuar_buscando:
            cursor = datos_json.get('nextCursor')
            if not cursor:
                 print("No se encontró nextCursor. Fin de los resultados.")
                 continuar_buscando = False

    # Guardado de los datos rescatados (incluso si hubo error a la mitad)
    print(f" Extracción finalizada. {len(ofertas_del_dia)} ofertas encontradas para el día objetivo.")
    
    if ofertas_del_dia:
        df = pd.DataFrame(ofertas_del_dia)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        archivo_csv = f"himalayas_raw_{fecha_objetivo_str}_{timestamp}.csv"
        df.to_csv(archivo_csv, index=False, encoding='utf-8')
        print(f"Archivo guardado en '{archivo_csv}'")
    else:
        print("No se extrajeron ofertas válidas.")

if __name__ == "__main__":
    # Asegúrate de buscar una fecha reciente para que no escanee toda la base de datos
    dia_a_extraer = "2026-11-02" 
    extraer_ofertas_por_dia(dia_a_extraer)