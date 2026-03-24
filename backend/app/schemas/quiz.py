from pydantic import BaseModel
from typing import List, Optional


class QuestionResponse(BaseModel):
    id: int
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    # Note: correct_option is NOT sent to client

    model_config = {"from_attributes": True}


class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    questions: List[QuestionResponse] = []

    model_config = {"from_attributes": True}


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str  # "a", "b", "c", "d"


class QuizSubmit(BaseModel):
    answers: List[AnswerSubmit]


class QuizResult(BaseModel):
    total_questions: int
    correct_answers: int
    score: int  # percentage
    xp_earned: int
