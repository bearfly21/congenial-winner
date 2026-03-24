from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, index=True)  # "occupation" or "school"
    subcategory = Column(String(100), nullable=True)  # "SMM", "Frontend", "Math", etc.
    image_url = Column(String(500), nullable=True)
    price = Column(Integer, default=0)  # in local currency, 0 = free
    discount_percent = Column(Integer, default=0)
    discount_start = Column(DateTime, nullable=True)
    discount_end = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    modules = relationship("Module", back_populates="course", order_by="Module.order")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    order = Column(Integer, default=0)

    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", order_by="Lesson.order")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String(500), nullable=True)  # YouTube URL or external link
    order = Column(Integer, default=0)

    # Relationships
    module = relationship("Module", back_populates="lessons")
