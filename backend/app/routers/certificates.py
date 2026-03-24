import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.progress import Progress, Badge
from app.models.course import Course
from app.models.progress import Enrollment
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/certificates", tags=["Certificates"])


@router.post("/generate")
def generate_certificate(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a PDF certificate for the current user."""
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor

    # Gather user data
    completed_count = (
        db.query(Progress)
        .filter(Progress.user_id == current_user.id, Progress.completed == True)
        .count()
    )
    badges = db.query(Badge).filter(Badge.user_id == current_user.id).all()
    enrolled_courses = (
        db.query(Course)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(Enrollment.user_id == current_user.id)
        .all()
    )

    # Generate PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Background
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(0, 0, width, height, fill=1)

    # Border
    c.setStrokeColor(HexColor("#e94560"))
    c.setLineWidth(3)
    c.rect(1.5 * cm, 1.5 * cm, width - 3 * cm, height - 3 * cm, fill=0)

    # Title
    c.setFillColor(HexColor("#e94560"))
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height - 4 * cm, "CERTIFICATE")

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 5.5 * cm, "This certificate is awarded to")

    # Name
    c.setFillColor(HexColor("#e94560"))
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(
        width / 2, height - 7.5 * cm,
        f"{current_user.first_name} {current_user.last_name}",
    )

    # Stats
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica", 12)
    y = height - 10 * cm
    c.drawCentredString(width / 2, y, f"XP: {current_user.xp}  |  Level: {current_user.level}  |  Lessons: {completed_count}")
    y -= 1 * cm

    if enrolled_courses:
        course_names = ", ".join(co.title for co in enrolled_courses[:3])
        c.drawCentredString(width / 2, y, f"Courses: {course_names}")
        y -= 1 * cm

    if badges:
        badge_names = ", ".join(f"{b.icon} {b.name}" for b in badges[:5])
        c.drawCentredString(width / 2, y, f"Badges: {badge_names}")

    # Footer
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#888888"))
    c.drawCentredString(width / 2, 2.5 * cm, "Omuz Learning Platform — omuz.uz")

    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=omuz_certificate_{current_user.id}.pdf"
        },
    )
