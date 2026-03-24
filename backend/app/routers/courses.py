from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.course import Course, Module, Lesson
from app.models.progress import Enrollment
from app.models.user import User
from app.schemas.course import CourseResponse, CourseListItem
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/courses", tags=["Courses"])


def _apply_discount(course: Course) -> Course:
    """Check if discount is currently active."""
    now = datetime.now(timezone.utc)
    if course.discount_start and course.discount_end:
        if not (course.discount_start <= now <= course.discount_end):
            course.discount_percent = 0
    return course


@router.get("/", response_model=list[CourseListItem])
def list_courses(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List all courses, optionally filtered by category."""
    query = db.query(Course)
    if category:
        query = query.filter(Course.category == category)
    courses = query.all()
    return [_apply_discount(c) for c in courses]


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get course details with modules and lessons."""
    course = (
        db.query(Course)
        .options(joinedload(Course.modules).joinedload(Module.lessons))
        .filter(Course.id == course_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return _apply_discount(course)


@router.post("/{course_id}/enroll")
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enroll current user in a course."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return {"message": "Successfully enrolled", "course_id": course_id}


@router.get("/{course_id}/enrolled")
def check_enrollment(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if current user is enrolled in a course."""
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id,
        )
        .first()
    )
    return {"enrolled": enrollment is not None}
