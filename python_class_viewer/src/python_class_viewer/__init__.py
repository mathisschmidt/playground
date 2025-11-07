import logging

from nicegui import ui
from .router import router
from .services.database_manager import DatabaseManager
from .utils.setup_logger import setup_advanced_logger
from .utils.var_env_manager import SingletonVarEnvManager


def main():
    # Set up logger
    logger = setup_advanced_logger(__name__, level=logging.DEBUG)
    logger.info(f"Starting Python Class Viewer server")

    logger.debug("Initializing database...")
    DatabaseManager.initialize_database()
    logger.debug("Checking environment variables...")
    SingletonVarEnvManager().check_availability()
    logger.debug("Getting NiceGUI router...")
    router()
    logger.info("Starting NiceGUI server on port 8080...")
    ui.run(port=SingletonVarEnvManager().port_server or 8080)