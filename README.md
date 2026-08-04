# Extractor y Almacenador Multivariable de Datos Atmosféricos en MySQL Remoto

## Descripción
Este proyecto consiste en un servicio automatizado e interactivo en Python que consulta en tiempo real variables meteorológicas de cualquier ubicación geográfica utilizando la API pública de **Open-Meteo**. El script traduce coordenadas (latitud y longitud) al nombre de la ubicación mediante geocodificación inversa (**Nominatim / OpenStreetMap**) y almacena las mediciones de forma estructurada e incremental en una base de datos **MySQL** remota alojada en **AlwaysData**.

El sistema almacena múltiples variables atmosféricas (`temperatura_c`, `humedad_pct`, `viento_kmh`, `presion_hpa`).

---

## Arquitectura del Sistema
```text
[ Entrada del Usuario: Coordenadas (Lat/Lon) ]
                       │
                       ▼
[ API Geocodificación: Nominatim / OSM ] ──► (Obtiene Nombre de la Ciudad)
                       │
                       ▼
[ API Meteorológica: Open-Meteo ] ─────────► (Consulta Multivariable)
                       │
                       ▼ (Extracción JSON)
             [ Script Python: main.py ]
                       │
                       ▼ (Conexión TCP/IP MySQL - Puerto 3306)
                [ MySQL DB ]
```

---

## Requisitos Previos
- Python 3.x instalado


## Configuración del Entorno Local
1. Instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

2. Duplicar el archivo `.env.example` y renombrarlo a `.env`:
```bash
cp .env.example .env
```

3. Completar las credenciales correspondientes a la base de datos en el archivo `.env`.
```bash
    DB_HOST=tu_host_aqui
    DB_USER=tu_usuario_aqui
    DB_PASSWORD=tu_password_aqui
    DB_NAME=tu_nombre_db_aqui
    DB_PORT=3306   
```

---

## Ejecución
```bash
python main.py
```