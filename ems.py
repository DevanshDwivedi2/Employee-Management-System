from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB = "employees.db"

def query(sql, args=(), fetch=False):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql, args)
    result = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

query("""
    CREATE TABLE IF NOT EXISTS employees (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT,
        salary     REAL,
        dob        TEXT,
        department TEXT
    )
""")

# Page 1 — Add Employee
@app.route("/")
def index():
    return render_template("index.html")

# Page 2 — View All Employees
@app.route("/employees-page")
def employees_page():
    return render_template("employees.html")

# API — Get all employees
@app.route("/employees")
def get_employees():
    rows = query("SELECT * FROM employees", fetch=True)
    employees = [
        {"id": r[0], "name": r[1], "salary": r[2], "dob": r[3], "department": r[4]}
        for r in rows
    ]
    return jsonify(employees)

# API — Add employee
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json
    query("INSERT INTO employees (name, salary, dob, department) VALUES (?, ?, ?, ?)",
          [data["name"], data["salary"], data["dob"], data["department"]])
    return jsonify({"message": "Added!"})

# API — Update employee
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    data = request.json
    query("UPDATE employees SET name=?, salary=?, dob=?, department=? WHERE id=?",
          [data["name"], data["salary"], data["dob"], data["department"], id])
    return jsonify({"message": "Updated!"})

# API — Delete employee
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    query("DELETE FROM employees WHERE id=?", [id])
    return jsonify({"message": "Deleted!"})

if __name__ == "__main__":
    app.run(debug=True)
app.config["MYSQL_PASSWORD"] = "1234"