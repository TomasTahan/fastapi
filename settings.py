# settings.py
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env (solo en desarrollo)
load_dotenv()

# Asigna las claves desde las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
