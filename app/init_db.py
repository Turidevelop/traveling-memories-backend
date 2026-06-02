"""
Módulo de inicialización de base de datos.

Este módulo se ejecuta cuando la aplicación inicia en Railway/Render,
asegurando que el esquema, tablas y permisos estén correctamente configurados.
"""

import os
import logging
from pathlib import Path
import asyncpg
from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError

logger = logging.getLogger(__name__)


async def init_database() -> None:
    """
    Inicializa la base de datos ejecutando scripts SQL en orden.
    
    Se ejecuta una sola vez al iniciar la aplicación.
    - Crea el esquema y tablas si no existen
    - Asigna permisos a usuarios de aplicación
    - Inserta datos iniciales (países, usuarios)
    
    Raises:
        Exception: Si hay error en la inicialización
    """
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.warning("DATABASE_URL no configurada, saltando init_db")
        return
    
    try:
        logger.info("🔐 Inicializando base de datos...")
        
        # Definir rutas de scripts SQL
        db_dir = Path(__file__).parent.parent / "DB"
        scripts = [
            db_dir / "03_create_schema_travel_and_tables.sql",
            db_dir / "02_grant_permissions.sql",
            db_dir / "04_insert_countries.sql",
            db_dir / "05_insert_into_appuser.sql",
        ]
        
        # Convertir DATABASE_URL de asyncpg a psycopg2 (sync)
        # postgresql+asyncpg://user:pass@host:port/db -> postgresql://user:pass@host:port/db
        sync_db_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
        
        # Crear engine de SQLAlchemy para ejecutar scripts
        engine = create_engine(sync_db_url)
        
        with engine.connect() as connection:
            for script_path in scripts:
                if not script_path.exists():
                    logger.warning(f"⚠️ Script no encontrado: {script_path}")
                    continue
                
                try:
                    with open(script_path, "r") as f:
                        sql_content = f.read()
                    
                    logger.info(f"📊 Ejecutando: {script_path.name}")
                    
                    # Dividir en statements individuales y ejecutar
                    # (algunos scripts tienen múltiples statements)
                    for statement in sql_content.split(";"):
                        statement = statement.strip()
                        if statement:  # Ignorar statements vacíos
                            try:
                                connection.execute(text(statement))
                            except ProgrammingError as e:
                                # Ignorar errores de "ya existe" (idempotente)
                                if "already exists" in str(e) or "duplicate" in str(e).lower():
                                    logger.debug(f"⏭️ {statement[:50]}... ya existe")
                                else:
                                    logger.error(f"❌ Error ejecutando statement: {e}")
                                    raise
                    
                    connection.commit()
                    logger.info(f"✅ {script_path.name} completado")
                    
                except Exception as e:
                    logger.error(f"❌ Error ejecutando {script_path.name}: {e}")
                    connection.rollback()
                    raise
        
        logger.info("✨ Base de datos inicializada correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error en init_database: {e}")
        raise

