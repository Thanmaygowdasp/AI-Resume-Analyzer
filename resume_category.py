def predict_category(found_skills):

    if (
        "Python" in found_skills and
        "Machine Learning" in found_skills
    ):
        return "Data Science"

    elif (
        "HTML" in found_skills and
        "CSS" in found_skills and
        "JavaScript" in found_skills
    ):
        return "Web Development"

    elif (
        "Java" in found_skills or
        "C++" in found_skills
    ):
        return "Software Development"

    else:
        return "General Technology"