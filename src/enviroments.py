import os
import secrets

DB_NAME = os.environ.get("DATABASE_TABLE", "mdliv_nuclear")
DB_TYPE = os.environ.get("DATABASE_TYPE", "postgresql")
SECRET_KEY = os.environ.get("SECRET_KEY", None)
if SECRET_KEY is None:
    try:
        with open("secret.txt") as f:
            SECRET_KEY = f.readline()
    except FileNotFoundError:
        with open("secret.txt", mode="w") as f:
            SECRET_KEY = secrets.token_urlsafe(16)
            f.write(SECRET_KEY)
DB_USER = os.environ.get('PG_USER', 'postgres')
DB_PASSWORD = os.environ.get('PG_PASSWORD', 'pgAdminPassword')
DB_PORT = os.environ.get('PG_PORT', 5432)
DB_HOST = os.environ.get('PG_HOST', 'localhost')

SITE_IP = os.environ.get("SITE_IP", "0.0.0.0")
SITE_PORT = int(os.environ.get("SITE_PORT", "8080"))
DEBUG = bool(os.environ.get("DEBUG", "False"))