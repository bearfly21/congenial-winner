from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# --- Lesson ---

class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    order: int = 0


class LessonResponse(LessonBase):
    id: int
    module_id: int

    model_config = {"from_attributes": True}


# --- Module ---

class ModuleBase(BaseModel):
    title: str
    order: int = 0


class ModuleResponse(ModuleBase):
    id: int
    course_id: int
    lessons: List[LessonResponse] = []

    model_config = {"from_attributes": True}


# --- Course ---

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    image_url: Optional[str] = None
    price: int = 0


class CourseResponse(CourseBase):
    id: int
    discount_percent: int = 0
    discount_start: Optional[datetime] = None
    discount_end: Optional[datetime] = None
    modules: List[ModuleResponse] = []

    model_config = {"from_attributes": True}


class CourseListItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    image_url: Optional[str] = None
    price: int
    discount_percent: int = 0

    model_config = {"from_attributes": True}
