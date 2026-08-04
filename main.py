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

def obtener_nombre_ubicacion(lat, lon):
    """Obtiene la ciudad y país usando la API de geocodificación gratuita de Nominatim"""
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&accept-language=es"
    headers = {"User-Agent": "MiProyectoBaseDatos_UNIS/1.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            
            # Busca la ciudad, pueblo, municipio o estado
            ciudad = address.get("city") or address.get("town") or address.get("village") or address.get("municipality") or address.get("state")
            pais = address.get("country", "")
            
            if ciudad and pais:
                return f"{ciudad}, {pais}"
            elif ciudad:
                return ciudad
    except Exception:
        pass
        
    return f"Lat: {lat}, Lon: {lon}"

def obtener_datos_clima_completos(lat, lon):
    """Consulta múltiples variables atmosféricas desde Open-Meteo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "surface_pressure"]
    }
    
    response = requests.get(url, params=params, timeout=10)
    if response.status_code == 200:
        current = response.json()["current"]
        return {
            "temp": current["temperature_2m"],
            "humedad": current["relative_humidity_2m"],
            "viento": current["wind_speed_10m"],
            "presion": current["surface_pressure"]
        }
    else:
        raise Exception(f"Error HTTP {response.status_code}")

def guardar_en_db(fuente, ciudad, temp, humedad, viento, presion):
    conn = None
    cursor = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Inserción limpia a columnas con sus unidades explícitas
        query = """
            INSERT INTO public_data (fuente, ciudad, temperatura_c, humedad_pct, viento_kmh, presion_hpa)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (fuente, ciudad, temp, humedad, viento, presion))
        conn.commit()
        
        hora_actual = time.strftime('%H:%M:%S')
        print(f"[{hora_actual}] 📍 {ciudad}")
        print(f" ├─ Temp: {temp} °C | Humedad: {humedad} %")
        print(f" └─ Viento: {viento} km/h | Presión: {presion} hPa\n")
        
    except mysql.connector.Error as err:
        print(f"Error en BD: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    print("=== Configuración del Nodo de Monitoreo Atmosférico ===")
    try:
        lat = float(input("Ingresa la latitud (ej. 14.63 para Cd. Guatemala): "))
        lon = float(input("Ingresa la longitud (ej. -90.51): "))
    except ValueError:
        print("Entrada no válida, asignando coordenadas por defecto (Ciudad de Guatemala)...")
        lat, lon = 14.63, -90.51

    print("Obteniendo nombre del lugar...")
    nombre_lugar = obtener_nombre_ubicacion(lat, lon)
    
    print(f"\nUbicación confirmada: {nombre_lugar}")
    print("Servicio activo. Guardando datos cada 60 segundos...\n")

    # String descriptivo de unidades para la base de datos
    UNIDADES = "°C, %, km/h, hPa"

    while True:
        try:
            clima = obtener_datos_clima_completos(lat, lon)
            guardar_en_db(
                fuente="Open-Meteo API",
                ciudad=nombre_lugar,
                temp=clima["temp"],
                humedad=clima["humedad"],
                viento=clima["viento"],
                presion=clima["presion"]
            )
        except Exception as e:
            print(f"Error en recolección: {e}")
            
        time.sleep(60)