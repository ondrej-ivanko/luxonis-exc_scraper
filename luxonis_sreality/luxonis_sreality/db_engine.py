import os
from sqlalchemy import create_engine
from sqlalchemy import URL


url = URL.create(
    drivername="postgresql",
    username=os.getenv("DB_USERNAME", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    database=os.getenv("DB_NAME", "sreality_apartments"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
)

engine = create_engine(url)
