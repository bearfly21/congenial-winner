from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base, SessionLocal

# Import all models so they register with Base.metadata
from app.models.user import User
from app.models.course import Course, Module, Lesson
from app.models.quiz import Quiz, Question
from app.models.progress import Enrollment, Progress, Badge, Notification

# Import routers
from app.routers import auth, courses, lessons, quizzes, gamification, certificates, notifications


def seed_data():
    """Insert sample data if database is empty."""
    db = SessionLocal()
    try:
        if db.query(Course).count() > 0:
            return  # Already seeded

        # --- Courses ---
        courses_data = [
            Course(
                title="Frontend разработка",
                description="Научитесь создавать современные веб-приложения с HTML, CSS и JavaScript. От основ до React.",
                category="occupation",
                subcategory="Frontend",
                image_url="https://images.unsplash.com/photo-1621839673705-6617adf9e890?w=400",
                price=0,
            ),
            Course(
                title="Backend на Python",
                description="Серверная разработка на Python: FastAPI, базы данных, REST API, деплой.",
                category="occupation",
                subcategory="Backend",
                image_url="https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400",
                price=50000,
            ),
            Course(
                title="SMM маркетинг",
                description="Продвижение в социальных сетях: стратегии, контент-план, таргетинг, аналитика.",
                category="occupation",
                subcategory="SMM",
                image_url="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400",
                price=30000,
            ),
            Course(
                title="UI/UX Дизайн",
                description="Основы дизайна интерфейсов: Figma, прототипирование, UX-исследования.",
                category="occupation",
                subcategory="Designer",
                image_url="https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400",
                price=40000,
            ),
            Course(
                title="AI и Machine Learning",
                description="Введение в искусственный интеллект: нейросети, NLP, компьютерное зрение.",
                category="occupation",
                subcategory="AI specialist",
                image_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400",
                price=60000,
            ),
            Course(
                title="Математика (8 класс)",
                description="Алгебра и геометрия для 8 класса: уравнения, функции, теоремы.",
                category="school",
                subcategory="Math",
                image_url="https://images.unsplash.com/photo-1635372722656-389f87a941b7?w=400",
                price=0,
            ),
            Course(
                title="English (Intermediate)",
                description="Английский язык: грамматика, лексика, аудирование, разговорная практика.",
                category="school",
                subcategory="English",
                image_url="https://images.unsplash.com/photo-1543109740-4bdb38fda756?w=400",
                price=25000,
            ),
        ]
        db.add_all(courses_data)
        db.flush()

        # --- Modules & Lessons for "Frontend разработка" ---
        m1 = Module(course_id=courses_data[0].id, title="HTML Основы", order=1)
        m2 = Module(course_id=courses_data[0].id, title="CSS Стилизация", order=2)
        m3 = Module(course_id=courses_data[0].id, title="JavaScript Базовый", order=3)
        db.add_all([m1, m2, m3])
        db.flush()

        lessons_data = [
            Lesson(module_id=m1.id, title="Что такое HTML?", description="Введение в HTML и структуру веб-страниц", video_url="https://www.youtube.com/watch?v=qz0aGYrrlhU", order=1),
            Lesson(module_id=m1.id, title="Теги и атрибуты", description="Основные HTML теги: заголовки, параграфы, списки", video_url="https://www.youtube.com/watch?v=UB1O30fR-EE", order=2),
            Lesson(module_id=m1.id, title="Формы и input", description="Создание форм и работа с пользовательским вводом", video_url="https://www.youtube.com/watch?v=fNcJuPIZ2WE", order=3),
            Lesson(module_id=m2.id, title="CSS Селекторы", description="Классы, ID, комбинаторы", video_url="https://www.youtube.com/watch?v=1PnVor36_40", order=1),
            Lesson(module_id=m2.id, title="Flexbox", description="Гибкая разметка с Flexbox", video_url="https://www.youtube.com/watch?v=JJSoEo8JSnc", order=2),
            Lesson(module_id=m3.id, title="Переменные и типы", description="let, const, типы данных в JavaScript", video_url="https://www.youtube.com/watch?v=W6NZfCO5SIk", order=1),
            Lesson(module_id=m3.id, title="Функции", description="Объявление и вызов функций, стрелочные функции", video_url="https://www.youtube.com/watch?v=xUI5Tsl2JpY", order=2),
        ]
        db.add_all(lessons_data)
        db.flush()

        # --- Quizzes ---
        quiz1 = Quiz(lesson_id=lessons_data[0].id, title="HTML Основы — Тест")
        db.add(quiz1)
        db.flush()

        questions_data = [
            Question(quiz_id=quiz1.id, text="Что означает HTML?", option_a="Hyper Text Markup Language", option_b="High Tech Machine Learning", option_c="Home Tool Markup Language", option_d="Hyper Transfer Markup Language", correct_option="a"),
            Question(quiz_id=quiz1.id, text="Какой тег используется для заголовка?", option_a="<p>", option_b="<h1>", option_c="<div>", option_d="<title>", correct_option="b"),
            Question(quiz_id=quiz1.id, text="Какой тег создает ссылку?", option_a="<link>", option_b="<href>", option_c="<a>", option_d="<url>", correct_option="c"),
        ]
        db.add_all(questions_data)

        # --- Modules & Lessons for "Backend на Python" ---
        m4 = Module(course_id=courses_data[1].id, title="Python Основы", order=1)
        m5 = Module(course_id=courses_data[1].id, title="FastAPI", order=2)
        db.add_all([m4, m5])
        db.flush()

        lessons_python = [
            Lesson(module_id=m4.id, title="Установка Python", description="Установка Python и настройка окружения", video_url="https://www.youtube.com/watch?v=YYXdXT2l-Gg", order=1),
            Lesson(module_id=m4.id, title="Синтаксис Python", description="Переменные, условия, циклы", video_url="https://www.youtube.com/watch?v=kqtD5dpn9C8", order=2),
            Lesson(module_id=m5.id, title="Первый API", description="Создание первого REST API на FastAPI", video_url="https://www.youtube.com/watch?v=0sOvCWFmrtA", order=1),
        ]
        db.add_all(lessons_python)

        db.commit()
        print("[OK] Seed data inserted successfully!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seed error: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and seed data on startup."""
    Base.metadata.create_all(bind=engine)
    seed_data()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Omuz — Online Learning Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Flutter app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod: restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(quizzes.router)
app.include_router(gamification.router)
app.include_router(certificates.router)
app.include_router(notifications.router)


@app.get("/")
def root():
    return {"message": "Welcome to Omuz API", "docs": "/docs"}
