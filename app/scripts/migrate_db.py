"""
Script para la migración de datos al nuevo esquema de base de datos.

Este script debe ejecutarse después de actualizar los modelos de SQLAlchemy
pero antes de iniciar la aplicación con la nueva estructura.
"""
import logging
import sys
import os

# Configurar la ruta para incluir el directorio raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.infrastructure.config.settings import Settings
from app.infrastructure.db.database import Base, engine
from app.infrastructure.db.models import UsuarioModel, ClienteModel, ProductoModel, OrdenDeTrabajoModel

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_database():
    """
    Realiza la migración de la base de datos del esquema antiguo al nuevo.
    """
    try:
        # Crear una sesión
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        logger.info("Iniciando migración de base de datos...")

        # Verificar si existen las tablas antiguas
        try:
            # Verificar si existe la tabla 'users'
            result = db.execute(text("SHOW TABLES LIKE 'users'"))
            has_users_table = result.fetchone() is not None

            if has_users_table:
                logger.info("Tabla 'users' encontrada. Iniciando migración de datos...")

                # 1. Migrar usuarios existentes a la nueva estructura
                # Primero, crear clientes por defecto para cada usuario
                db.execute(text("""
                    INSERT INTO tableCLIENTE (nombreCLIENTE, fecha_movCLIENTE)
                    SELECT name, created_at FROM users
                    GROUP BY name
                """))
                db.commit()

                # 2. Asociar usuarios a los clientes creados y migrar sus datos
                db.execute(text("""
                    INSERT INTO tableUSUARIO 
                    (idCLIENTE_FK, nombre_completoUSUARIO, emailUSUARIO, passwordUSUARIO, fecha_movUSUARIO)
                    SELECT 
                        c.idCLIENTE, 
                        u.name, 
                        u.email, 
                        u.password_hash, 
                        u.created_at
                    FROM users u
                    JOIN tableCLIENTE c ON c.nombreCLIENTE = u.name
                """))
                db.commit()

                logger.info("Migración de usuarios completada")

                # 3. Crear productos de ejemplo (opcional)
                db.execute(text("""
                    INSERT INTO tablePRODUCTO (tipoPRODUCTO, descripcionPRODUCTO, precioPRODUCTO)
                    VALUES 
                        ('Tipo1', 'Producto de ejemplo 1', 100.00),
                        ('Tipo2', 'Producto de ejemplo 2', 150.00),
                        ('Tipo3', 'Producto de ejemplo 3', 200.00)
                """))
                db.commit()

                logger.info("Productos de ejemplo creados")
            else:
                logger.info("No se encontró la tabla 'users'. La base de datos está limpia.")

                # Crear datos de ejemplo para desarrollo
                if input("¿Desea crear datos de ejemplo para desarrollo? (s/n): ").lower() == 's':
                    create_sample_data(db)

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error al verificar o migrar las tablas: {str(e)}")
            raise

        logger.info("Migración completada exitosamente")

    except Exception as e:
        logger.error(f"Error durante la migración: {str(e)}", exc_info=True)
        raise
    finally:
        db.close()


def create_sample_data(db):
    """
    Crea datos de ejemplo para desarrollo.
    """
    try:
        logger.info("Creando datos de ejemplo...")

        # 1. Crear clientes
        clientes = [
            ClienteModel(nombreCLIENTE="Cliente de Prueba 1"),
            ClienteModel(nombreCLIENTE="Cliente de Prueba 2"),
            ClienteModel(nombreCLIENTE="Cliente de Prueba 3")
        ]
        db.add_all(clientes)
        db.commit()

        # 2. Crear usuarios
        usuarios = [
            UsuarioModel(
                idCLIENTE_FK=1,
                nombre_completoUSUARIO="Usuario Prueba 1",
                emailUSUARIO="usuario1@ejemplo.com",
                passwordUSUARIO="$2b$12$1xxxxxxxxxxxxxxxxxxxxuXxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                # Hash de bcrypt para "password"
                numero_clienteUSUARIO="001"
            ),
            UsuarioModel(
                idCLIENTE_FK=2,
                nombre_completoUSUARIO="Usuario Prueba 2",
                emailUSUARIO="usuario2@ejemplo.com",
                passwordUSUARIO="$2b$12$1xxxxxxxxxxxxxxxxxxxxuXxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                # Hash de bcrypt para "password"
                numero_clienteUSUARIO="002"
            )
        ]
        db.add_all(usuarios)
        db.commit()

        # 3. Crear productos
        productos = [
            ProductoModel(tipoPRODUCTO="Tipo1", descripcionPRODUCTO="Producto de ejemplo 1", precioPRODUCTO=100.00),
            ProductoModel(tipoPRODUCTO="Tipo2", descripcionPRODUCTO="Producto de ejemplo 2", precioPRODUCTO=150.00),
            ProductoModel(tipoPRODUCTO="Tipo3", descripcionPRODUCTO="Producto de ejemplo 3", precioPRODUCTO=200.00)
        ]
        db.add_all(productos)
        db.commit()

        # 4. Crear órdenes de trabajo
        ordenes = [
            OrdenDeTrabajoModel(
                idCLIENTE_FK=1,
                idPRODUCTO_FK=1,
                statusORDENDETRABAJO="pendiente",
                idPRODUCTO_linea1=1,
                cantidadPRODUCTO_linea1=2,
                precio_unitarioPRODUCTO_linea1=100.00
            ),
            OrdenDeTrabajoModel(
                idCLIENTE_FK=2,
                idPRODUCTO_FK=2,
                statusORDENDETRABAJO="en proceso",
                idPRODUCTO_linea1=2,
                cantidadPRODUCTO_linea1=1,
                precio_unitarioPRODUCTO_linea1=150.00
            )
        ]
        db.add_all(ordenes)
        db.commit()

        logger.info("Datos de ejemplo creados exitosamente")

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear datos de ejemplo: {str(e)}")
        raise

    if __name__ == "__main__":
        # Crear las tablas en la base de datos
        try:
            logger.info("Creando tablas en la base de datos...")
            Base.metadata.create_all(bind=engine)
            logger.info("Tablas creadas exitosamente")

            # Ejecutar migración
            migrate_database()

        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            sys.exit(1)