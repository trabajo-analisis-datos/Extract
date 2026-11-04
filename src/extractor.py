import requests
from datetime import datetime
import time

def extraer_ofertas_himalayas(fecha_objetivo_str, limite_maximo=1000):
    """
    Se conecta a la API, pagina mediante cursores y extrae las ofertas de un día.
    Retorna los datos crudos en memoria para inyectarlos al pipeline.
    """
    url = "https://himalayas.app/jobs/api"
    ofertas_extraidas = []
    
    limit = 20
    cursor = None
    continuar_extrayendo = True
    max_reintentos = 5
    
    fecha_objetivo = datetime.strptime(fecha_objetivo_str, "%Y-%m-%d").date()
    print(f"[EXTRACTOR] Iniciando escaneo de API para el {fecha_objetivo_str}...")
    
    # Mantiene un solo túnel TCP abierto, optimizando los tiempos de respuesta
    session = requests.Session()
    
    while continuar_extrayendo:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
            
        intentos = 0
        exito_peticion = False
        
        while intentos < max_reintentos and not exito_peticion:
            try:
                response = session.get(url, params=params, timeout=15)
                response.raise_for_status()
                datos = response.json()
                exito_peticion = True
            except requests.exceptions.RequestException as e:
                intentos += 1
                print(f"  Inestabilidad de red (Intento {intentos}/{max_reintentos}). Reconectando...")
                time.sleep(3)
        
        if not exito_peticion:
            print("   Conexión perdida irreversiblemente. Retornando datos rescatados.")
            break
            
        ofertas_pagina = datos.get('jobs', [])
        if not ofertas_pagina:
            break
            
        for oferta in ofertas_pagina:
            fecha_ts = oferta.get('pubDate')
            if fecha_ts:
                fecha_oferta = datetime.fromtimestamp(fecha_ts).date()
                
                # Reglas de negocio para la fecha
                if fecha_oferta == fecha_objetivo:
                    ofertas_extraidas.append(oferta)
                    if len(ofertas_extraidas) >= limite_maximo:
                        continuar_extrayendo = False
                        break
                elif fecha_oferta < fecha_objetivo:
                    # Himalayas ordena de más nuevo a más viejo. 
                    # Si llegamos a ayer, ya no hay más ofertas de hoy.
                    continuar_extrayendo = False
                    break
        
        if continuar_extrayendo:
            cursor = datos.get('nextCursor')
            if not cursor:
                 continuar_extrayendo = False

    print(f"[EXTRACTOR] Proceso finalizado: {len(ofertas_extraidas)} ofertas crudas cargadas en memoria.")
    return ofertas_extraidas