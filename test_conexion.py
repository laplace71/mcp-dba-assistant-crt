import sys
import src.config
from src.database import obtener_conexion_dinamica

def probar_conexion(bd, servidor=None):
    print(f"\nConectando a '{bd}'...")
    try:
        conn = obtener_conexion_dinamica(bd, servidor)
        print(f"[OK] ¡Conexión exitosa a {bd}!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 3 name FROM sys.tables ORDER BY name")
        tablas = cursor.fetchall()
        
        if tablas:
            print(f"Primeras 3 tablas encontradas:")
            for t in tablas:
                print(f"  - {t[0]}")
        else:
            print("No se encontraron tablas.")
            
        conn.close()
    except Exception as e:
        print(f"\n[ERROR] Falló la conexión:")
        print(f"{type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python test_conexion.py <BaseDeDatos> [Servidor]")
        print("Ejemplo 1 (Normal): python test_conexion.py SRContabilidad")
        print("Ejemplo 2 (Duplicada): python test_conexion.py msdb PuntoVenta")
        sys.exit(1)
        
    base = sys.argv[1]
    serv = sys.argv[2] if len(sys.argv) > 2 else None
    
    probar_conexion(base, serv)
