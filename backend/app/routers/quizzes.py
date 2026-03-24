from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.quiz import Quiz, Question
from app.models.progress import Progress
from app.models.user import User
from app.schemas.quiz import QuizResponse, QuizSubmit, QuizResult
from app.services.gamification import add_xp, check_and_award_badges
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/quizzes", tags=["Quizzes"])


@router.get("/{lesson_id}", response_model=QuizResponse)
def get_quiz_for_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get quiz questions for a lesson (without correct answers)."""
    quiz = (
        db.query(Quiz)
        .options(joinedload(Quiz.questions))
        .filter(Quiz.lesson_id == lesson_id)
        .first()
    )
    if not quiz:
        raise HTTPException(status_code=404, detail="No quiz for this lesson")
    return quiz


@router.post("/{quiz_id}/submit", response_model=QuizResult)
def submit_quiz(
    quiz_id: int,
    data: QuizSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit quiz answers and get results."""
    quiz = (
        db.query(Quiz)
        .options(joinedload(Quiz.questions))
        .filter(Quiz.id == quiz_id)
        .first()
    )
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Build correct answers map
    correct_map = {q.id: q.correct_option for q in quiz.questions}
    total = len(correct_map)
    correct = 0

    for answer in data.answers:
        if correct_map.get(answer.question_id) == answer.selected_option:
            correct += 1

    score = int((correct / total) * 100) if total > 0 else 0

    # Save quiz score to progress
    progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == current_user.id,
            Progress.lesson_id == quiz.lesson_id,
        )
        .first()
    )
    if not progress:
        progress = Progress(
            user_id=current_user.id,
            lesson_id=quiz.lesson_id,
            quiz_score=score,
            completed_at=datetime.now(timezone.utc),
        )
        db.add(progress)
    else:
        progress.quiz_score = score

    db.commit()

    # Award XP (+20 for passing quiz, minimum 50% to pass)
    xp_earned = 0
    if score >= 50:
        xp_earned = 20
        add_xp(current_user, xp_earned, db)
        check_and_award_badges(current_user, db)

    return QuizResult(
        total_questions=total,
        correct_answers=correct,
        score=score,
        xp_earned=xp_earned,
    )
