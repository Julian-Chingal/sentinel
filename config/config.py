import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    # ── Carpetas ──────────────────────────────
    DIR_WATCH      = os.getenv("DIR_WATCH",      "./watch")     
    DIR_PROCESADO  = os.getenv("DIR_PROCESADO",  "./procesado")  
    DIR_ERRORES    = os.getenv("DIR_ERRORES",    "./errores")   
    LOG_DIR        = os.getenv("LOG_DIR",        "./logs")

    # ── Base de datos ─────────────────────────
    DB_HOST        = os.getenv("DB_HOST",        "localhost")
    DB_PORT        = int(os.getenv("DB_PORT",    "3306"))
    DB_USER        = os.getenv("DB_USER",        "root")
    DB_PASSWORD    = os.getenv("DB_PASSWORD",    "")
    DB_NAME        = os.getenv("DB_NAME",        "mi_base")

    # ── Comportamiento ────────────────────────
    # Segundos a esperar antes de leer el archivo (evita leer mientras se escribe)
    WAIT_SECONDS   = float(os.getenv("WAIT_SECONDS", "1.5"))
