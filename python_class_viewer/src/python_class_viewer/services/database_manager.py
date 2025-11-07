import logging

from sqlmodel import SQLModel, Session, create_engine
from ..utils.var_env_manager import SingletonVarEnvManager

logger = logging.getLogger(__name__)

class DatabaseManager:
    _engine = None
    _database_url: str = "sqlite:///upload_info.db"

    @classmethod
    def change_url(cls, url: str):
        cls._database_url = url
        cls._engine = None
        cls.get_engine()

    @classmethod
    def get_engine(cls):
        """Get or create the database engine."""
        if cls._engine is None:
            logger.info("Creating database engine with URL: %s", cls._database_url)
            cls._engine = create_engine(
                cls._database_url,
                echo=False,  # Set to True for SQL debugging
                connect_args={"check_same_thread": False}  # For SQLite
            )
            # Create tables
            SQLModel.metadata.create_all(cls._engine)
        return cls._engine

    @classmethod
    def get_session(cls) -> Session:
        """Get a new database session."""
        return Session(cls.get_engine())

    @classmethod
    def initialize_database(cls):
        if database_url := SingletonVarEnvManager().database_url:
            cls.change_url(database_url)
        cls.get_engine()