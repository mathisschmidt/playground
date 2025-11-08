from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, select
from python_class_viewer.services.database_manager import DatabaseManager


class UploadInfo(SQLModel, table=True):
    """
    Stores metadata about uploaded files for analysis.
    Tracks file information and code metrics extracted from uploaded files.
    """
    __tablename__ = "upload_info"

    id: Optional[UUID] = Field(
        default_factory=uuid4,  # Python fallback - works on ALL databases
        primary_key=True,
        description="Unique identifier for the upload, auto-generated"
    )

    file_name: str = Field(
        max_length=255,
        description="Name of the file uploaded"
    )

    file_size: float = Field(
        gt=0,
        description="Size of the file in kilobytes (KB)"
    )

    number_class: int = Field(
        ge=0,
        description="Total number of classes defined in the file"
    )

    number_relation: int = Field(
        ge=0,
        description="Total number of relationships between classes (inheritance, composition, etc.)"
    )

    number_property: int = Field(
        ge=0,
        description="Total number of properties/attributes across all classes"
    )

    number_methods: int = Field(
        ge=0,
        description="Total number of methods/functions defined in the file"
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the record was created"
    )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "file_name": self.file_name,
            "file_size": self.file_size,
            "number_class": self.number_class,
            "number_relation": self.number_relation,
            "number_property": self.number_property,
            "number_methods": self.number_methods,
            "created_at": self.created_at.isoformat()
        }

    @staticmethod
    def get_by_id(upload_id: UUID) -> Optional[UploadInfo]:
        """
        Get upload info by ID.

        Args:
            upload_id: UUID of the upload

        Returns:
            UploadInfo instance or None if not found
        """
        with DatabaseManager.get_session() as session:
            return session.get(UploadInfo, upload_id)

    @staticmethod
    def get_all(limit: Optional[int] = None, offset: int = 0) -> list[UploadInfo]:
        """
        Get all upload info records.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of UploadInfo instances
        """
        with DatabaseManager.get_session() as session:
            stmt = select(UploadInfo).offset(offset)
            if limit:
                stmt = stmt.limit(limit)
            return list(session.exec(stmt).all())

    @staticmethod
    def get_by_filename(file_name: str) -> list[UploadInfo]:
        """
        Get all uploads with a specific filename.

        Args:
            file_name: Name of the file

        Returns:
            List of UploadInfo instances
        """
        with DatabaseManager.get_session() as session:
            stmt = select(UploadInfo).where(UploadInfo.file_name == file_name)
            return list(session.exec(stmt).all())

    @staticmethod
    def search_by_filename(pattern: str) -> list[UploadInfo]:
        """
        Search uploads by filename pattern (case-insensitive).

        Args:
            pattern: Search pattern (e.g., "%.py" or "%test%")

        Returns:
            List of matching UploadInfo instances
        """
        with DatabaseManager.get_session() as session:
            stmt = select(UploadInfo).where(UploadInfo.file_name.like(f"%{pattern}%"))
            return list(session.exec(stmt).all())

    @staticmethod
    def get_by_size_range(min_size: float, max_size: float) -> list[UploadInfo]:
        """
        Get uploads within a size range.

        Args:
            min_size: Minimum file size in KB
            max_size: Maximum file size in KB

        Returns:
            List of UploadInfo instances
        """
        with DatabaseManager.get_session() as session:
            stmt = select(UploadInfo).where(
                UploadInfo.file_size >= min_size,
                UploadInfo.file_size <= max_size
            )
            return list(session.exec(stmt).all())

    @staticmethod
    def get_complex_files(min_classes: int = 5) -> list[UploadInfo]:
        """
        Get files with high complexity (many classes).

        Args:
            min_classes: Minimum number of classes

        Returns:
            List of UploadInfo instances
        """
        with DatabaseManager.get_session() as session:
            stmt = select(UploadInfo).where(
                UploadInfo.number_class >= min_classes
            ).order_by(UploadInfo.number_class.desc())
            return list(session.exec(stmt).all())

    @staticmethod
    def delete_all() -> int:
        """
        Delete all upload info records.

        Returns:
            Number of records deleted
        """
        with DatabaseManager.get_session() as session:
            stmt = select(UploadInfo)
            uploads = session.exec(stmt).all()
            count = len(uploads)

            for upload in uploads:
                session.delete(upload)

            session.commit()
            return count