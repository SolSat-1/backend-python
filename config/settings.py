from dotenv import load_dotenv

from config.util import Environment

# from logger import logger
import logging


""""load environment variables"""
# Load env variables from a file, if exists else default would be set
logger = logging.getLogger(__name__)
logger.info("SERVER_INIT::Setting environment variables from .env file(if exists)...")
load_dotenv(verbose=True)
# load_dotenv(dotenv_path=".env", verbose=True)


class DB:
    host = Environment.get_string("DB_HOST", "postgres_db")
    port = Environment.get_string("DB_PORT", "5432")
    name = Environment.get_string("DB_NAME", "test")
    user = Environment.get_string("DB_USER", "root")
    pass_ = Environment.get_string("DB_PASS", "password")


class JWTToken:
    algorithm = Environment.get_string("JWT_ALGORITHM", "HS256")
    secret = Environment.get_string("JWT_SECRET", "secret")
    access_token_expire_minutes = Environment.get_string(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "86400"
    )


class HuggingFace:
    API_KEY = Environment.get_string("HUGGINGFACE_API_KEY", "API_KEY")


class COMMON:
    environment = Environment.get_string("ENVIRONMENT", "development")
    log_level = Environment.get_string("LOG_LEVEL", "DEBUG")
    is_local = Environment.get_string("IS_LOCAL", "True")
