from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
from predictor.mutation_predictor import MutationPredictor
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "super_secret_key"

predictor = MutationPredictor()
DB = "users.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                (name, email, password, role)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            return render_template("signup.html", error="Email already exists")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = email
            return redirect(url_for("predictor_page"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/predictor")
def predictor_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("predictor.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    ref_seq = request.form["reference"]
    query_seq = request.form["sequence"]

    result = predictor.analyze(ref_seq, query_seq)
    session["last_result"] = result

    return render_template("result.html", result=result)

@app.route("/visualize")
def visualize():
    result = session.get("last_result")
    if not result:
        return redirect(url_for("predictor_page"))
    return render_template("visualize.html", result=result)

@app.route("/download")
def download():
    r = session.get("last_result")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for k, v in r.items():
        pdf.cell(0, 10, f"{k}: {v}", ln=True)

    path = "mutation_result.pdf"
    pdf.output(path)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
