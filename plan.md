# OMUZ PLATFORM — Plan

## Tech Stack

| Слой | Технология | Обоснование |
|------|-----------|-------------|
| **Mobile App** | **Flutter 3** (Dart) | Один код → Android + iOS + Web. Нативная производительность |
| **Backend** | **FastAPI** (Python 3.11+) | Async, авто-документация Swagger, быстрая разработка |
| **ORM** | **SQLAlchemy 2.0** + Alembic | Абстракция БД — переключение SQLite ↔ PostgreSQL без изменений кода |
| **Database (dev)** | **SQLite** | Не нужен сервер, быстрый старт |
| **Database (prod)** | **PostgreSQL 16** | Надёжная, масштабируемая |
| **Auth** | OTP mock + JWT | По ТЗ: без паролей |
| **State (Flutter)** | **Provider** | Простой, достаточный для MVP |
| **HTTP (Flutter)** | **Dio** | HTTP клиент с интерцепторами |
| **PDF** | **ReportLab** | Генерация сертификатов |

> **Важно:** SQLAlchemy ORM абстрагирует базу данных. Весь код пишется через ORM — смена SQLite → PostgreSQL = одна строка в `.env`.

---

## Структура проекта

```
omuz/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── alembic/
│   ├── .env
│   └── requirements.txt
├── frontend/    (Flutter)
│   ├── lib/
│   │   ├── main.dart
│   │   ├── config/
│   │   ├── models/
│   │   ├── providers/
│   │   ├── screens/
│   │   ├── services/
│   │   └── widgets/
│   └── pubspec.yaml
├── plan.md
└── tz.md
```

---

## Database Schema

```
USER: id, phone, first_name, last_name, xp, level, streak_days, last_active, is_admin
COURSE: id, title, description, category, image_url, price, discount_percent, discount_start, discount_end
MODULE: id, course_id (FK), title, order
LESSON: id, module_id (FK), title, description, video_url, order
QUIZ: id, lesson_id (FK), title
QUESTION: id, quiz_id (FK), text, option_a/b/c/d, correct_option
ENROLLMENT: id, user_id (FK), course_id (FK), enrolled_at
PROGRESS: id, user_id (FK), lesson_id (FK), completed, quiz_score, completed_at
BADGE: id, user_id (FK), name, icon, earned_at
NOTIFICATION: id, user_id (FK), title, message, is_read, created_at
```

---

## API Endpoints

| # | Method | Path | Описание |
|---|--------|------|----------|
| 1 | POST | `/api/auth/send-otp` | Отправить OTP |
| 2 | POST | `/api/auth/verify-otp` | Верификация → JWT |
| 3 | GET | `/api/auth/me` | Текущий юзер |
| 4 | GET | `/api/courses` | Список курсов |
| 5 | GET | `/api/courses/{id}` | Детали курса |
| 6 | POST | `/api/courses/{id}/enroll` | Записаться |
| 7 | GET | `/api/lessons/{id}` | Данные урока |
| 8 | POST | `/api/lessons/{id}/complete` | Завершить урок (+XP) |
| 9 | GET | `/api/quizzes/{lesson_id}` | Квиз для урока |
| 10 | POST | `/api/quizzes/{id}/submit` | Ответы → результат |
| 11 | GET | `/api/gamification/profile` | XP, уровень, бейджи |
| 12 | GET | `/api/gamification/leaderboard` | Топ студентов |
| 13 | POST | `/api/certificates/generate` | PDF сертификат |
| 14 | GET | `/api/notifications` | Уведомления |

---

## Фазы реализации

| # | Фаза | Что делаем | Приоритет |
|---|------|-----------|-----------|
| 1 | **Каркас** | Backend + DB модели + Flutter scaffold | 🔴 |
| 2 | **Auth** | OTP mock + JWT + Login screen | 🔴 |
| 3 | **Курсы** | CRUD + список + детали | 🔴 |
| 4 | **Уроки** | API + экран урока + YouTube | 🔴 |
| 5 | **Квизы** | API + экран квиза | 🟡 |
| 6 | **Геймификация** | XP, бейджи, лидерборд | 🟡 |
| 7 | **Сертификаты** | PDF генерация | 🟡 |
| 8 | **Скидки + Уведомления** | Бонусные фичи | 🟢 |
| 9 | **Полировка** | UI/UX, анимации | 🟢 |

> После каждой фазы — тестирование: запуск backend + frontend, проверка работоспособности.
