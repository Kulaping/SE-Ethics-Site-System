import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def log_info(console):
    return logger.info(console)

def log_warning(console_warning):
    return logger.warning(console_warning)