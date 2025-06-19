from flask import Flask, render_template, request, redirect
import mysql.connector
from flask import flash, get_flashed_messages



app = Flask(__name__, template_folder='templates')
app.secret_key = "your_secret_key_here"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # 🔁 Replace this!
    database="student_db"
)
cursor = conn.cursor()

@app.route('/')
def home():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template('home.html', students=data)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        name = name.title()  # "john doe" becomes "John Doe"
        email = request.form['email']
        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("⚠️ This email is already registered!")
            return redirect(url_for('add_student'))

        phone = request.form['phone']
        if not (phone.isdigit() and len(phone) == 10):
            return "Invalid phone number. Must be exactly 10 digits."

        cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        flash("✅ Student added successfully!")
        return redirect(url_for('home'))
    return render_template('add_student.html')
from flask import redirect, url_for

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="student_db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
