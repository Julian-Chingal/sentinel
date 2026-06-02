# Sentinel

Sentinel es un sistema de monitorización de directorios escrito en Python. Está diseñado para estar "escuchando" constantemente una carpeta específica en el servidor. Cuando detecta que un nuevo archivo ha sido subido y guardado por completo (100%), lo procesa como texto plano, consulta información en una base de datos MySQL, inserta un registro y finalmente mueve el archivo a una carpeta de "procesados" o "errores" dependiendo del resultado.

## Arquitectura y Flujo

1. **Monitorización**: `main.py` utiliza la librería `watchdog` para vigilar el directorio configurado (`watch/` por defecto).
2. **Validación de Archivo**: Antes de procesar, el sistema se asegura de que el archivo haya sido escrito en su totalidad verificando que su tamaño en disco deje de cambiar.
3. **Procesamiento**: En `sentinel/processor.py`, el sistema lee el archivo sin importar su extensión (ej. `z456784.001`) como un archivo de texto plano.
4. **Base de Datos**: Se extraen los datos del archivo y se hace uso de `utils/connection.py` para:
   - Consultar información en 2 tablas distintas de la base de datos.
   - Insertar un nuevo registro en una tercera tabla.
5. **Clasificación**: 
   - Si todo fue exitoso, el archivo original es movido a la carpeta `procesado/`.
   - Si ocurrió algún error (en lectura, conexión, o formato), el archivo es movido a la carpeta `errores/`.

## Requisitos Previos

- Python 3.8+
- MySQL Server

## Instalación y Configuración

1. **Crear y activar un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar las variables de entorno**:
   Crea un archivo `.env` en la raíz del proyecto (donde está `main.py`) con las siguientes variables. Ajusta los valores según tu servidor de base de datos:
   
   ```env
   # Rutas (opcional, si no se definen usarán los valores por defecto)
   DIR_WATCH=./watch
   DIR_PROCESADO=./procesado
   DIR_ERRORES=./errores
   LOG_DIR=./logs

   # Conexión a Base de Datos
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   DB_NAME=tu_base_de_datos
   ```

4. **Completar Lógica de Negocio (TO-DO)**:
   - **Mapeo de Datos:** Dirígete a `sentinel/processor.py` y edita la función `_extract_data()` para que extraiga los datos que necesitas de cada archivo.
   - **Sentencias SQL:** Dirígete a `utils/connection.py` y edita las funciones `query_table_1()`, `query_table_2()` e `insert_record()` con el nombre real de tus tablas y columnas.

## Uso

Para iniciar el sistema centinela, simplemente ejecuta:

```bash
python main.py
```

Verás un mensaje en consola indicando que el sistema ha iniciado. A partir de ese momento, cualquier archivo que dejes caer en la carpeta `watch/` será procesado automáticamente.

## Pruebas (Testing)

El proyecto cuenta con pruebas unitarias usando `pytest` para verificar el correcto funcionamiento del procesador simulando escenarios de éxito y error con la base de datos. 

Para correr las pruebas, ejecuta:
```bash
python -m pytest tests
```
