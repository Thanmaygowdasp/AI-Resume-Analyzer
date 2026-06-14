from skills import skills

def calculate_ats_score(found_skills):

    ats_score = round(
        (len(found_skills) / len(skills)) * 100
    )

    missing_skills = []

    for skill in skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    return ats_score, missing_skills