from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.progress import Progress, Badge
from app.schemas.gamification import GamificationProfile, BadgeResponse, LeaderboardEntry
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/gamification", tags=["Gamification"])


@router.get("/profile", response_model=GamificationProfile)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get gamification profile for current user."""
    badges = db.query(Badge).filter(Badge.user_id == current_user.id).all()
    completed_lessons = (
        db.query(Progress)
        .filter(Progress.user_id == current_user.id, Progress.completed == True)
        .count()
    )
    completed_quizzes = (
        db.query(Progress)
        .filter(
            Progress.user_id == current_user.id,
            Progress.quiz_score.isnot(None),
        )
        .count()
    )

    return GamificationProfile(
        xp=current_user.xp,
        level=current_user.level,
        streak_days=current_user.streak_days,
        badges=[BadgeResponse.model_validate(b) for b in badges],
        completed_lessons=completed_lessons,
        completed_quizzes=completed_quizzes,
    )


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    """Get top 20 students by XP."""
    users = db.query(User).order_by(desc(User.xp)).limit(20).all()
    return [
        LeaderboardEntry(
            rank=i + 1,
            user_id=u.id,
            first_name=u.first_name,
            last_name=u.last_name,
            xp=u.xp,
            level=u.level,
        )
        for i, u in enumerate(users)
    ]
