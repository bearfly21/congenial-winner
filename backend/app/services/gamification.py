"""
Gamification Service — XP, levels, badges.
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.progress import Badge


# XP thresholds for levels
LEVEL_THRESHOLDS = [0, 50, 150, 300, 500, 800, 1200, 1700, 2300, 3000]

# Badge definitions
BADGE_DEFINITIONS = {
    "first_lesson": {"name": "Первый урок", "icon": "🎓", "condition": lambda u, db: _count_completed(u, db) >= 1},
    "five_lessons": {"name": "5 уроков", "icon": "📚", "condition": lambda u, db: _count_completed(u, db) >= 5},
    "ten_lessons": {"name": "10 уроков", "icon": "🏆", "condition": lambda u, db: _count_completed(u, db) >= 10},
    "first_quiz": {"name": "Первый тест", "icon": "✅", "condition": lambda u, db: _count_quizzes(u, db) >= 1},
    "streak_3": {"name": "3 дня подряд", "icon": "🔥", "condition": lambda u, db: u.streak_days >= 3},
    "streak_7": {"name": "Неделя подряд", "icon": "⚡", "condition": lambda u, db: u.streak_days >= 7},
    "xp_100": {"name": "100 XP", "icon": "💯", "condition": lambda u, db: u.xp >= 100},
    "xp_500": {"name": "500 XP", "icon": "🌟", "condition": lambda u, db: u.xp >= 500},
}


def _count_completed(user: User, db: Session) -> int:
    from app.models.progress import Progress
    return db.query(Progress).filter(
        Progress.user_id == user.id,
        Progress.completed == True,
    ).count()


def _count_quizzes(user: User, db: Session) -> int:
    from app.models.progress import Progress
    return db.query(Progress).filter(
        Progress.user_id == user.id,
        Progress.quiz_score.isnot(None),
    ).count()


def add_xp(user: User, amount: int, db: Session) -> int:
    """Add XP to user. Recalculate level. Returns new XP total."""
    user.xp += amount
    # Recalculate level
    new_level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if user.xp >= threshold:
            new_level = i + 1
    user.level = new_level
    db.commit()
    return user.xp


def check_and_award_badges(user: User, db: Session) -> list:
    """Check all badge conditions and award any new ones."""
    existing = {b.name for b in db.query(Badge).filter(Badge.user_id == user.id).all()}
    awarded = []
    for key, badge_def in BADGE_DEFINITIONS.items():
        if badge_def["name"] not in existing and badge_def["condition"](user, db):
            badge = Badge(
                user_id=user.id,
                name=badge_def["name"],
                icon=badge_def["icon"],
            )
            db.add(badge)
            awarded.append(badge_def["name"])
    if awarded:
        db.commit()
    return awarded


def calculate_level(xp: int) -> int:
    """Calculate level from XP."""
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
    return level
