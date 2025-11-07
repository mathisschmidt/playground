from sqlmodel import SQLModel, Session, create_engine

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