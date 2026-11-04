import os
import json

def guardar_ofertas_json(ofertas, fecha_str):
    """
    Crea un directorio dinámico en la carpeta 'data/' y guarda cada oferta 
    como un archivo JSON individual utilizando su identificador único (guid).
    """
    if not ofertas:
        print("[PERSISTENCIA] No hay ofertas para guardar.")
        return

    print(f"[PERSISTENCIA] Iniciando guardado de {len(ofertas)} archivos individuales...")

    # 1. Definir rutas relativas de forma robusta
    # os.path.abspath(__file__) ubica dónde está este script (en /src)
    # os.path.dirname retrocede un nivel para llegar a la raíz del proyecto
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    directorio_raiz = os.path.dirname(directorio_script)
    directorio_destino = os.path.join(directorio_raiz, 'data', f'jobs_{fecha_str}')

    # 2. Crear el directorio si no existe (exist_ok=True evita que de error si ya está creado)
    os.makedirs(directorio_destino, exist_ok=True)

    # 3. Guardar cada oferta iterando la lista
    archivos_guardados = 0
    for oferta in ofertas:
        # El ID único de la oferta en la API de Himalayas es el 'guid'
        id_unico = oferta.get('guid')
        
        # Fallback de seguridad: si alguna oferta viniera sin guid
        if not id_unico:
            id_unico = f"id_faltante_{archivos_guardados}"
            
        # Reemplazar caracteres que el sistema operativo prohíbe en nombres de archivo
        id_limpio = str(id_unico).replace('/', '_').replace('\\', '_')
        ruta_archivo = os.path.join(directorio_destino, f"{id_limpio}.json")
        
        # Guardar en formato JSON puro
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo_json:
            # ensure_ascii=False asegura que las tildes y caracteres en español se guarden bien
            json.dump(oferta, archivo_json, indent=4, ensure_ascii=False)
            
        archivos_guardados += 1
        
    print(f"  Guardado exitoso: {archivos_guardados} archivos generados en '{directorio_destino}'.")