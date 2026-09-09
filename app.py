from flask import Flask, render_template, request

app = Flask(__name__)


# ==============================
# ROLE REQUIREMENTS
# ==============================

role_requirements = {
    "Python Developer": {
        "Python": 4,
        "SQL": 3,
        "HTML": 2,
        "Communication": 3,
        "Problem Solving": 4
    },

    "Data Analyst": {
        "Python": 3,
        "SQL": 4,
        "HTML": 1,
        "Communication": 3,
        "Problem Solving": 4
    },

    "Web Developer": {
        "Python": 2,
        "SQL": 3,
        "HTML": 4,
        "Communication": 3,
        "Problem Solving": 3
    }
}


# ==============================
# LEARNING RECOMMENDATIONS
# ==============================

recommendations = {
    "Python": "Complete Python programming and problem-solving practice.",
    "SQL": "Learn SQL queries, joins, grouping and database operations.",
    "HTML": "Practice HTML structure, forms and web page development.",
    "Communication": "Practice presentation, teamwork and professional communication.",
    "Problem Solving": "Practice algorithms, logical problems and coding challenges."
}


# ==============================
# HOME
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# ANALYZE
# ==============================

@app.route("/analyze", methods=["POST"])
def analyze():

    name = request.form["name"]

    skills = {
        "Python": int(request.form["python"]),
        "SQL": int(request.form["sql"]),
        "HTML": int(request.form["html"]),
        "Communication": int(request.form["communication"]),
        "Problem Solving": int(request.form["problem_solving"])
    }

    role = request.form["role"]


    # =================================
    # FIND BEST ROLE
    # =================================

    if role == "Find My Best Role":

        role_scores = []

        for role_name, required in role_requirements.items():

            total_score = 0

            for skill, required_level in required.items():

                employee_level = skills[skill]

                score = min(
                    employee_level / required_level,
                    1
                )

                total_score += score

            readiness = round(
                (total_score / len(required)) * 100
            )

            role_scores.append({
                "role": role_name,
                "score": readiness
            })


        role_scores.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        best_role = role_scores[0]["role"]


        return render_template(
            "matches.html",
            name=name,
            role_scores=role_scores,
            best_role=best_role
        )


    # =================================
    # NORMAL ROLE ANALYSIS
    # =================================

    required = role_requirements[role]

    gaps = []

    total_score = 0


    for skill, required_level in required.items():

        employee_level = skills[skill]


        # Find skill gap

        if employee_level < required_level:

            gaps.append({
                "skill": skill,
                "current": employee_level,
                "required": required_level
            })


        # Calculate score

        score = min(
            employee_level / required_level,
            1
        )

        total_score += score


    # =================================
    # READINESS
    # =================================

    readiness = round(
        (total_score / len(required)) * 100
    )


    # =================================
    # LEARNING PATH
    # =================================

    learning_path = []


    for gap in gaps:

        learning_path.append(
            recommendations[gap["skill"]]
        )


    # =================================
    # SEND EVERYTHING TO result.html
    # =================================

    return render_template(
        "result.html",
        name=name,
        role=role,
        readiness=readiness,
        gaps=gaps,
        learning_path=learning_path
    )


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)