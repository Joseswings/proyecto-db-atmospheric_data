# Extractor y Almacenador de Datos Públicos en MySQL Remoto

## Descripción
Este proyecto consiste en un servicio automatizado en Python que realiza peticiones periódicas a la API pública de **Open-Meteo** para obtener mediciones atmosféricas en tiempo real (temperatura en °C) y las almacena de manera estructurada e incremental en una base de datos **MySQL** alojada en la nube mediante el servicio de hosting **AlwaysData** (administrada visualmente vía **phpMyAdmin**).

El sistema implementa buenas prácticas de desarrollo para la gestión segura de credenciales mediante el uso de variables de entorno y archivos de configuración excluidos del control de versiones.

---

## Arquitectura del Sistema
```text
[ API Pública: Open-Meteo ] 
         │
         ▼ (Petición HTTP GET / JSON)
[ Script Python: main.py ] 
         │
         ▼ (Conexión TCP/IP MySQL - Puerto 3306)
[ MySQL DB / phpMyAdmin en AlwaysData ]
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


## Ejecución
```bash
python main.py
```