import re
from pypdf import PdfReader
from skills import skills


def analyze_resume(uploaded_file):

    score = 0

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    cleaned_text = re.sub(
        r"\s+",
        "",
        text.lower()
    )

    found_skills = []

    for skill in skills:

        skill_clean = skill.lower().replace(
            " ",
            ""
        )

        if skill_clean in cleaned_text:
            found_skills.append(skill)

    education_found = "education" in cleaned_text

    projects_found = (
        "project" in cleaned_text
        or "projects" in cleaned_text
    )

    github_found = "github" in cleaned_text

    # Score Calculation

    if education_found:
        score += 15

    if projects_found:
        score += 20

    if github_found:
        score += 15

    skill_count = len(found_skills)

    if skill_count >= 8:
        score += 40
    elif skill_count >= 5:
        score += 30
    elif skill_count >= 3:
        score += 20
    elif skill_count >= 1:
        score += 10
        

    return {
        "text": text,
        "found_skills": found_skills,
        "education_found": education_found,
        "projects_found": projects_found,
        "github_found": github_found,
        "score": score,
        "pages": len(reader.pages)
    }