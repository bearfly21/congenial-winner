from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Lesson
from app.models.progress import Progress
from app.models.user import User
from app.schemas.course import LessonResponse
from app.services.gamification import add_xp, check_and_award_badges
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/lessons", tags=["Lessons"])


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get lesson data (video URL, description)."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark lesson as completed and award XP."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Check if already completed
    progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == current_user.id,
            Progress.lesson_id == lesson_id,
        )
        .first()
    )
    if progress and progress.completed:
        return {"message": "Lesson already completed", "xp_earned": 0}

    # Create or update progress
    if not progress:
        progress = Progress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            completed=True,
            completed_at=datetime.now(timezone.utc),
        )
        db.add(progress)
    else:
        progress.completed = True
        progress.completed_at = datetime.now(timezone.utc)

    db.commit()

    # Award XP (+10 for completing a lesson)
    xp_earned = 10
    new_xp = add_xp(current_user, xp_earned, db)
    badges = check_and_award_badges(current_user, db)

    return {
        "message": "Lesson completed!",
        "xp_earned": xp_earned,
        "total_xp": new_xp,
        "new_badges": badges,
    }
