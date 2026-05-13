"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    
    # Leer el archivo línea por línea
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Procesar datos
    data = []
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = ""
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        
        # Buscar línea que comienza con número de cluster (ignorando espacios)
        # Formato: "   1     105             15,9 %          maximum power..."
        patron_cluster = r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)'
        match = re.match(patron_cluster, line)
        
        if match:
            # Guardar cluster anterior si existe
            if current_cluster is not None:
                # Limpiar keywords del cluster anterior
                keywords_clean = re.sub(r'\s+', ' ', current_keywords.strip())
                keywords_clean = re.sub(r'\s*,\s*', ', ', keywords_clean)
                keywords_clean = keywords_clean.rstrip(',.')
                data.append([current_cluster, current_cantidad, current_porcentaje, keywords_clean])
            
            # Nuevo cluster
            current_cluster = int(match.group(1))
            current_cantidad = int(match.group(2))
            # Reemplazar coma por punto en el porcentaje
            porcentaje_str = match.group(3).replace(',', '.')
            current_porcentaje = float(porcentaje_str)
            # Palabras clave iniciales
            current_keywords = match.group(4).strip()
        else:
            # Línea de continuación de palabras clave (con indentación)
            if current_cluster is not None and line.strip():
                # Agregar la línea completa como continuación de keywords
                current_keywords += " " + line.strip()
        
        i += 1
    
    # Guardar el último cluster
    if current_cluster is not None:
        keywords_clean = re.sub(r'\s+', ' ', current_keywords.strip())
        keywords_clean = re.sub(r'\s*,\s*', ', ', keywords_clean)
        keywords_clean = keywords_clean.rstrip(',.')
        data.append([current_cluster, current_cantidad, current_porcentaje, keywords_clean])
    
    # Crear DataFrame
    df = pd.DataFrame(data, columns=[
        'cluster',
        'cantidad_de_palabras_clave',
        'porcentaje_de_palabras_clave',
        'principales_palabras_clave'
    ])
    
    return df