import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde la ruta absoluta del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Las configuraciones como timeouts y drivers se pueden definir aquí 
# si decides no usar os.getenv repetidamente. Por ahora, cargar .env
# al inicio es el objetivo principal de este módulo.
