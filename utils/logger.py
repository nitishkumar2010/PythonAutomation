import logging

logging.basicConfig(
    level=logging.DEBUG,  # Ensure logs appear
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Prints logs to terminal
)

logger = logging.getLogger(__name__)  # Use a module-level logger
