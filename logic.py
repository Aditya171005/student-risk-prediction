def get_insights(studytime, failures, absences, health):
    reasons = []
    tips = []

    if failures > 1:
        reasons.append("High number of past failures")
        tips.append("Focus on weak subjects and revision")

    if absences > 10:
        reasons.append("Too many absences")
        tips.append("Improve attendance consistency")

    if studytime < 2:
        reasons.append("Low study time")
        tips.append("Increase daily study hours")

    if health < 3:
        reasons.append("Health may affect performance")
        tips.append("Maintain proper sleep and nutrition")

    return reasons, tips