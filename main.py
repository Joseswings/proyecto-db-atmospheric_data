import os
import time
import requests
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def obtener_datos_publicos():
    """Obtiene la temperatura actual desde la API pública de Open-Meteo"""
    # Coordenadas para Ciudad de Guatemala
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 14.63,
        "longitude": -90.51,
        "current": "temperature_2m"
    }
    headers = {
        "User-Agent": "MiProyectoBaseDatos/1.0"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        temp = data["current"]["temperature_2m"]
        return "Open-Meteo", "Temperatura", temp, "°C"
    else:
        raise Exception(f"Error HTTP {response.status_code}: {response.text}")

def guardar_en_db(fuente, variable, valor, unidad):
    conn = None
    cursor = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO public_data (fuente, variable, valor, unidad)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (fuente, variable, valor, unidad))
        conn.commit()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Dato insertado con éxito: {valor} {unidad}")
        
    except mysql.connector.Error as err:
        print(f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def ejecutar_tarea():
    print("Recolectando datos...")
    try:
        fuente, var, val, uni = obtener_datos_publicos()
        guardar_en_db(fuente, var, val, uni)
    except Exception as e:
        print(f"Fallo en la ejecución: {e}")

if __name__ == "__main__":
    ejecutar_tarea()
    
    INTERVALO_SEGUNDOS = 60
    print(f"Servicio activo. Actualizando cada {INTERVALO_SEGUNDOS} segundos... (Presiona Ctrl+C para salir)")
    
    while True:
        time.sleep(INTERVALO_SEGUNDOS)
        ejecutar_tarea()
