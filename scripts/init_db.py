import os
import sys
import logging
import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://resolveai:resolveai_secret@localhost:5432/resolveai_db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "warehouse", "schema.sql")


def init_db():
    logger.info("Connecting to database: %s", DATABASE_URL)
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            sql = f.read()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Successfully initialized ResolveAI database schema.")
    except Exception as e:
        logger.error("Failed to initialize database schema: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    init_db()
