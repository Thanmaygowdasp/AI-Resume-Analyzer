def recommend_roles(found_skills):

    roles = []

    if "Python" in found_skills:
        roles.append("Python Developer")

    if "Java" in found_skills:
        roles.append("Java Developer")

    if "SQL" in found_skills:
        roles.append("Database Developer")

    if (
        "Python" in found_skills and
        "Machine Learning" in found_skills
    ):
        roles.append("Machine Learning Engineer")

    if (
        "Python" in found_skills and
        "Data Science" in found_skills
    ):
        roles.append("Data Scientist")

    if (
        "HTML" in found_skills and
        "CSS" in found_skills and
        "JavaScript" in found_skills
    ):
        roles.append("Frontend Developer")

    if (
        "React" in found_skills and
        "Node.js" in found_skills
    ):
        roles.append("Full Stack Developer")

    if "Linux" in found_skills:
        roles.append("System Administrator")

    return list(set(roles))