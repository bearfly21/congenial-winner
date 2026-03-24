from sqlalchemy import Column, Integer, String, Boolean, DateTime, func


from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    # Gamification
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak_days = Column(Integer, default=0)
    last_active = Column(DateTime, server_default=func.now())

    # Role
    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.phone} — {self.first_name}>"
