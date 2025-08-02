from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env
def get_env_variable(key: str, default=None):
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    return os.getenv(key, default)
