from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


# Bảng liên kết nhiều-nhiều giữa todos và tags
todo_tags = Table(
    "todo_tags",
    Base.metadata,
    Column("todo_id", Integer, ForeignKey("todos.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


class Tag(Base):
    """SQLAlchemy model cho bảng tags"""
    
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    color = Column(String(7), default="#3B82F6")  # Hex color
    
    # Owner - mỗi user có tags riêng
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", backref="tags")
    todos = relationship("ToDo", secondary=todo_tags, back_populates="tags")


class ToDo(Base):
    """SQLAlchemy model cho bảng todos"""
    
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False, nullable=False)
    due_date = Column(Date, nullable=True)  # Deadline
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Foreign key to users
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="todos")
    tags = relationship("Tag", secondary=todo_tags, back_populates="todos")
    
    @property
    def is_deleted(self) -> bool:
        """Check if todo is soft deleted"""
        return self.deleted_at is not None
