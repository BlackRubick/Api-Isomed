"""
Script para inicializar la base de datos MySQL.
"""
import pymysql
from app.infrastructure.config.settings import Settings

settings = Settings()


def init_database():
    """
    Inicializa la base de datos MySQL creando la base de datos si no existe.
    """
    # Extraer nombre de la base de datos desde la URL
    connection_info = settings.DATABASE_URL.replace("mysql+pymysql://", "")
    credentials, db_info = connection_info.split("@")

    username, password = credentials.split(":")
    host_port, db_name = db_info.split("/")

    if ":" in host_port:
        host, port = host_port.split(":")
        port = int(port)
    else:
        host = host_port
        port = 3306

    # Conectar a MySQL sin especificar una base de datos
    connection = pymysql.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        charset="utf8mb4"
    )

    try:
        with connection.cursor() as cursor:
            # Crear la base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"Base de datos '{db_name}' creada o verificada exitosamente.")

            # Usar la base de datos
            cursor.execute(f"USE {db_name};")

            # Crear el usuario para la aplicación si es diferente a root
            if username != "root":
                try:
                    cursor.execute(f"CREATE USER IF NOT EXISTS '{username}'@'%' IDENTIFIED BY '{password}';")
                    cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'%';")
                    cursor.execute("FLUSH PRIVILEGES;")
                    print(f"Usuario '{username}' creado y configurado exitosamente.")
                except Exception as e:
                    print(f"Advertencia al configurar usuario: {e}")

        connection.commit()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    init_database()
    print("Inicialización de la base de datos completada.")