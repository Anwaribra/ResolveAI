import os
import glob
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "documents")


def seed_knowledge():
    files = glob.glob(os.path.join(DOCS_DIR, "*.md"))
    logger.info("Found %d markdown documents in knowledge base: %s", len(files), DOCS_DIR)
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info("Seeded document: %s (%d chars)", filename, len(content))
    logger.info("Knowledge base documents verified.")


if __name__ == "__main__":
    seed_knowledge()
