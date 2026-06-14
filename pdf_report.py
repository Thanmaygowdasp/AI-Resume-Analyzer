from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_report(
    score,
    ats_score,
    found_skills,
    missing_skills,
    roles,
    feedback
):

    pdf_file = "resume_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Resume Score: {score}/100",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"ATS Score: {ats_score}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Detected Skills:",
            styles["Heading2"]
        )
    )

    for skill in found_skills:
        content.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Missing Skills:",
            styles["Heading2"]
        )
    )

    for skill in missing_skills:
        content.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Recommended Roles:",
            styles["Heading2"]
        )
    )

    for role in roles:
        content.append(
            Paragraph(
                f"• {role}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "AI Feedback:",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            feedback,
            styles["Normal"]
        )
    )

    doc.build(content)

    return pdf_file