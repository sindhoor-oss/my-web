from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------------- ROLE REQUIREMENTS ----------------

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


# ---------------- LEARNING RECOMMENDATIONS ----------------

recommendations = {
    "Python": "Complete Python programming and problem-solving practice.",
    "SQL": "Learn SQL queries, joins, grouping and database operations.",
    "HTML": "Practice HTML structure, forms and web page development.",
    "Communication": "Practice presentation, teamwork and professional communication.",
    "Problem Solving": "Practice algorithms, logical problems and coding challenges."
}


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            python INTEGER,
            sql INTEGER,
            html INTEGER,
            communication INTEGER,
            problem_solving INTEGER,
            readiness INTEGER
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ANALYZE ----------------

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


    # -------- FIND BEST ROLE --------

    if role == "Find My Best Role":

        role_scores = []

        for role_name, required in role_requirements.items():

            total_score = 0

            for skill, required_level in required.items():

                employee_level = skills[skill]

                score = min(employee_level / required_level, 1)

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

        # Save best role result
        best_score = role_scores[0]["score"]

        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO employees
            (
                name,
                role,
                python,
                sql,
                html,
                communication,
                problem_solving,
                readiness
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            best_role,
            skills["Python"],
            skills["SQL"],
            skills["HTML"],
            skills["Communication"],
            skills["Problem Solving"],
            best_score
        ))

        conn.commit()
        conn.close()

        return render_template(
            "matches.html",
            name=name,
            role_scores=role_scores,
            best_role=best_role
        )


    # -------- SELECTED ROLE --------

    required = role_requirements[role]

    gaps = []

    total_score = 0

    for skill, required_level in required.items():

        employee_level = skills[skill]

        if employee_level < required_level:

            gaps.append({
                "skill": skill,
                "current": employee_level,
                "required": required_level
            })

        score = min(
            employee_level / required_level,
            1
        )

        total_score += score


    readiness = round(
        (total_score / len(required)) * 100
    )


    # -------- LEARNING PATH --------

    learning_path = []

    for gap in gaps:

        learning_path.append(
            recommendations[gap["skill"]]
        )


    # -------- SAVE FINAL DATA --------

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees
        (
            name,
            role,
            python,
            sql,
            html,
            communication,
            problem_solving,
            readiness
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        role,
        skills["Python"],
        skills["SQL"],
        skills["HTML"],
        skills["Communication"],
        skills["Problem Solving"],
        readiness
    ))

    conn.commit()
    conn.close()


    return render_template(
        "result.html",
        name=name,
        role=role,
        readiness=readiness,
        gaps=gaps,
        learning_path=learning_path
    )


# ---------------- ADMIN DATA PAGE ----------------

@app.route("/admin")
def admin():

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            role,
            python,
            sql,
            html,
            communication,
            problem_solving,
            readiness
        FROM employees
        ORDER BY id DESC
    """)

    employees = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        employees=employees
    )


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )