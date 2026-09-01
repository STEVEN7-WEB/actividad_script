# Protocolo de Gestión y Procesamiento Masivo de Datos Ambientales

Este repositorio contiene los scripts y la configuración necesarios para la ingesta y procesamiento masivo de datos ambientales provenientes de diversas dependencias gubernamentales. El proyecto forma parte de las actividades para el manejo de datos en el contexto de investigación ambiental.

Todo el entorno de base de datos está contenedorizado utilizando Docker y MongoDB para su ejecución local.

## 🗄️ Acceso a la Base de Datos (Revisión)

Dado que la infraestructura está montada en Docker con la imagen `mongo:latest`, no hay un enlace externo. Para revisar los datos cargados, levanta los servicios y conéctate de forma local:

* **Motor:** MongoDB
* **Host:** `localhost` (o `127.0.0.1`)
* **Puerto:** `27017`
* **Autenticación:** Sin usuario ni contraseña (configuración por defecto para desarrollo local).

## 🛠️ Estructura del Proyecto

* `main_ingesta.py`: Script principal en Python encargado de procesar los datasets y realizar la carga masiva hacia MongoDB.
* `docker-compose.yml`: Archivo de configuración para levantar el contenedor `mongodb_ambiental`.

## 🚀 Requisitos y Ejecución

Para probar el script, es necesario contar con **Docker**, **Docker Compose** y **Python 3.x**.

1. **Levantar la base de datos:**
   Abre una terminal en esta carpeta y ejecuta:
   ```bash
   docker-compose up -d
