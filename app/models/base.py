from datetime import datetime
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    """
    Base model for all SQLModel models.
    This class provides a common base for all models,
    allowing for shared functionality and attributes.
    """
    __abstract__ = True

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    @classmethod
    def __tablename__(cls) -> str:
        """
        Override the __tablename__ method to return the table name.
        This method is used by SQLModel to determine the table name for the model.
        """
        return cls.__name__.lower()
