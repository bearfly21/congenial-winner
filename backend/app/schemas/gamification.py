from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class GamificationProfile(BaseModel):
    xp: int
    level: int
    streak_days: int
    badges: List["BadgeResponse"] = []
    completed_lessons: int
    completed_quizzes: int


class BadgeResponse(BaseModel):
    id: int
    name: str
    icon: str
    earned_at: datetime

    model_config = {"from_attributes": True}


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    first_name: str
    last_name: str
    xp: int
    level: int
