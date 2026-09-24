import os
import pyodbc
from src.utils import parse_bool, parse_positive_int

def obtener_conexion_dinamica(base_datos: str, servidor: str = None) -> pyodbc.Connection:
    """Obtiene una conexión segura y dinámica mapeando la BD a su servidor físico y credenciales."""
    db_upper = base_datos.strip().upper()
    
    # 1. Encontrar el servidor asociado a esta BD (considerando si hay parámetro servidor)
    if servidor:
        srv_upper = servidor.strip().upper()
        
        # --- NORMALIZADOR DE ALIAS ---
        # Permite a Claude (o al usuario) escribir como quiera, el sistema lo corrige.
        if srv_upper in ["PUNTOVENTA", "PUNTO VENTA", "PV", "PUNTO_VENTA"]:
            srv_upper = "PV"
        elif srv_upper in ["SOPORTE", "SOPORTECRT"]:
            srv_upper = "SOPORTE"
            
        server_env_key = f"MAP_{db_upper}_{srv_upper}_SERVER"
        user_env_key = f"CRED_{db_upper}_{srv_upper}_USER"
        pass_env_key = f"CRED_{db_upper}_{srv_upper}_PASSWORD"
    else:
        server_env_key = f"MAP_{db_upper}_SERVER"
        user_env_key = f"CRED_{db_upper}_USER"
        pass_env_key = f"CRED_{db_upper}_PASSWORD"

    server_name = os.getenv(server_env_key)
    if not server_name:
        if servidor:
            raise ValueError(f"Base de datos '{base_datos}' en el servidor '{servidor}' no está mapeada en la configuración (.env). Falta {server_env_key}")
        else:
            raise ValueError(
                f"ERROR CRÍTICO PARA LA IA: La base de datos '{base_datos}' no tiene una conexión por defecto. "
                f"Esto significa que es una base de datos repetida. DETENTE INMEDIATAMENTE y pregúntale al usuario "
                f"a qué conexión/servidor desea ir (por ejemplo: 'PuntoVenta' o 'Soporte'). Luego, usa el parámetro 'servidor'."
                f"Opciones de servidor: 'PuntoVenta' o 'Soporte'."
            )
    
    # 2. Encontrar el host del servidor
    host_env_key = f"{server_name}_HOST"
    host = os.getenv(host_env_key)
    if not host:
        raise ValueError(f"No se encontró el host para el servidor {server_name}. Falta {host_env_key}")
        
    # 3. Encontrar credenciales
    user = os.getenv(user_env_key)
    password = os.getenv(pass_env_key)
    
    if not user or not password:
        raise ValueError(f"Faltan credenciales para la base de datos '{base_datos}'. Revisar {user_env_key} y {pass_env_key}")

    # 4. Configuración general
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").strip("{} ")
    trust_cert = parse_bool(os.getenv("SQLSERVER_TRUST_CERT", "true"))
    query_timeout = parse_positive_int(os.getenv("QUERY_TIMEOUT_SECONDS", "30"), "QUERY_TIMEOUT_SECONDS")
    
    # 5. Construir y retornar conexión
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={host};"
        f"DATABASE={base_datos};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        f"TrustServerCertificate={'yes' if trust_cert else 'no'};"
        "ApplicationIntent=ReadOnly;"
    )
    
    return pyodbc.connect(
        connection_string,
        autocommit=True,
        timeout=query_timeout
    )
