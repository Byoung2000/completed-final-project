from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Dragon'

class Config:
    SECRET_KEY = 'Dragon'

# Database Configuration
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="flask_user",
        password="password",
        database="fitness_tracker"
    )

# Routes

@app.route('/')
def index():
    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id, username, email FROM Users")
            users = cursor.fetchall()
        return render_template('index.html', users=users)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('error.html')

@app.route('/user/<int:user_id>')
def user_detail(user_id):
    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT goal_id, goal_name, goal_type, goal_target, progress FROM Goals WHERE user_id = %s", (user_id,))
            goals = cursor.fetchall()

            cursor.execute("SELECT activity_id, activity_date, activity_value FROM Activities WHERE goal_id IN (SELECT goal_id FROM Goals WHERE user_id = %s)", (user_id,))
            activities = cursor.fetchall()

        return render_template('user_detail.html', goals=goals, activities=activities, user_id=user_id)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('error.html')

@app.route('/add_goal/<int:user_id>', methods=['POST'])
def add_goal(user_id):
    try:
        goal_name = request.form.get('goal_name')
        goal_type = request.form.get('goal_type')
        goal_target = request.form.get('goal_target')

        if not all((goal_name, goal_type, goal_target)):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('user_detail', user_id=user_id))

        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO Goals (user_id, goal_name, goal_type, goal_target, progress) VALUES (%s, %s, %s, %s, 0)",
                           (user_id, goal_name, goal_type, goal_target))
            db.commit()

        flash('Goal added successfully!', 'success')
        return redirect(url_for('user_detail', user_id=user_id))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('user_detail', user_id=user_id))

@app.route('/update_goal/<int:user_id>/<int:goal_id>', methods=['POST'])
def update_goal(user_id, goal_id):
    try:
        new_goal_name = request.form.get('new_goal_name')
        new_goal_type = request.form.get('new_goal_type')
        new_goal_target = request.form.get('new_goal_target')

        if not all((new_goal_name, new_goal_type, new_goal_target)):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('user_detail', user_id=user_id))

        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Goals WHERE goal_id = %s", (goal_id,))
            goal = cursor.fetchone()

            if not goal:
                flash('Goal not found.', 'error')
                return redirect(url_for('user_detail', user_id=user_id))

            cursor.execute("UPDATE Goals SET goal_name = %s, goal_type = %s, goal_target = %s WHERE goal_id = %s",
                           (new_goal_name, new_goal_type, new_goal_target, goal_id))
            db.commit()

        flash('Goal updated successfully!', 'success')
        return redirect(url_for('user_detail', user_id=user_id))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('user_detail', user_id=user_id))

@app.route('/delete_goal/<int:user_id>/<int:goal_id>', methods=['POST'])
def delete_goal(user_id, goal_id):
    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Goals WHERE goal_id = %s", (goal_id,))
            goal = cursor.fetchone()

            if not goal:
                flash('Goal not found.', 'error')
                return redirect(url_for('user_detail', user_id=user_id))

            cursor.execute("DELETE FROM Goals WHERE goal_id = %s", (goal_id,))
            db.commit()

        flash('Goal deleted successfully!', 'success')
        return redirect(url_for('user_detail', user_id=user_id))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('user_detail', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)
