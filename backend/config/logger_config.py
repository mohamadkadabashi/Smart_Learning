from loguru import logger
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent 
LOG_DIR = BASE_DIR / "logs" 

LOG_DIR.mkdir(parents=True, exist_ok=True)

# Remove default configuration
logger.remove()

# Console output configuration
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)

# File for INFO logs (includes WARNING, ERROR, CRITICAL)
logger.add(
    "logs/info.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="INFO",
    enqueue=True
)

# File for ERROR logs only
logger.add(
    "logs/error.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="ERROR",
    enqueue=True
)
