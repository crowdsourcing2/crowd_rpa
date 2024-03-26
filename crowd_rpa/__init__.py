import logging
from colorlog import ColoredFormatter
from crowd_rpa.api import make_collector, make_extractor

# Configure the logging settings with color
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

# Get the root logger
logger = logging.getLogger()

# Remove any existing handlers to avoid duplication
logger.handlers.clear()

# Set the logging level
logger.setLevel(logging.INFO)

# Add a new handler with the specified formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)