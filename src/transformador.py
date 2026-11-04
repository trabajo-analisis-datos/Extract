def filtrar_solo_tecnologia(ofertas):
    """
    Filtra las ofertas para dejar solo las relacionadas con Informática/Tecnología,
    utilizando el parámetro 'categories' de la API de Himalayas.
    """
    print("[TRANSFORMADOR] Aplicando filtro de TI...")
    ofertas_ti = []
    
    # Categorías tecnológicas clave según la estructura de Himalayas
    categorias_ti = ['Software Engineering', 'Data', 'Product', 'DevOps', 'Web3', 'Security']
    
    for oferta in ofertas:
        categorias_oferta = oferta.get('categories', [])
        
        if categorias_oferta:
            # Verifica si hay intersección entre las categorías de la oferta y las nuestras
            es_ti = any(cat in categorias_oferta for cat in categorias_ti)
            if es_ti:
                ofertas_ti.append(oferta)
                
    print(f"   Filtro aplicado: Quedaron {len(ofertas_ti)} ofertas de tecnología (de un total de {len(ofertas)}).")
    return ofertas_ti

def estandarizar_estructura_json(ofertas):
    """
    Garantiza que TODOS los diccionarios (JSONs) tengan exactamente las mismas llaves.
    Si a una oferta le falta un parámetro que otra sí tiene, se le inyecta con valor None (null).
    """
    if not ofertas:
        return []
    
    print("🛠️ [TRANSFORMADOR] Estandarizando modelo de dominio (rellenando nulos)...")
    
    # 1. Identificar el universo total de llaves presentes en la extracción completa
    todas_las_llaves = set()
    for oferta in ofertas:
        todas_las_llaves.update(oferta.keys())
        
    # 2. Reconstruir cada oferta forzando la presencia de todas las llaves
    ofertas_estandarizadas = []
    for oferta in ofertas:
        oferta_uniforme = {}
        for llave in todas_las_llaves:
            # .get() devuelve None automáticamente si la llave no existe en ese registro específico
            oferta_uniforme[llave] = oferta.get(llave, None)
        ofertas_estandarizadas.append(oferta_uniforme)
        
    print(f"   Estandarización completa: Cada registro posee ahora exactamente {len(todas_las_llaves)} parámetros simétricos.")
    return ofertas_estandarizadas