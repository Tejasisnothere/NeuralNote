import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


logger = logging.getLogger("NeuralNote")
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = logging.FileHandler(LOG_DIR/"app.log")
file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(console_handler)

