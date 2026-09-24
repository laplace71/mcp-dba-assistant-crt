import src.config  # Importar config primero garantiza que load_dotenv() se ejecute antes de hacer cualquier cosa
from mcp.server.fastmcp import FastMCP
from src.tools import registrar_herramientas

# Inicializar servidor MCP con el nuevo nombre de asistente DBA
mcp = FastMCP("SQLServer-DBA-Assistant-MCP")

# Registrar todas las herramientas
registrar_herramientas(mcp)

if __name__ == "__main__":
    mcp.run()
