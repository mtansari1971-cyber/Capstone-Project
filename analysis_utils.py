import pandas as pd


def create_skill_dataframe(skill_analysis):

    data = []

    for skill in skill_analysis:

        data.append({
            "Skill": skill.skill,
            "Status": skill.status,
            "Importance": skill.importance
        })

    return pd.DataFrame(data)


def create_bullet_dataframe(weak_bullets):

    data = []

    for bullet in weak_bullets:

        data.append({
            "Original": bullet.original,
            "Problem": bullet.problem,
            "Improved": bullet.improved
        })

    return pd.DataFrame(data)


def score_label(score):

    if score >= 90:
        return "Excellent"

    elif score >= 80:
        return "Very Good"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Needs Improvement"

    return "Poor"