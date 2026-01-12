# Configure logging
import logging

logging.basicConfig(
    level=logging.INFO,  # Show INFO and higher level logs
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)
