from flask import Flask, request, jsonify, render_template
import pymysql
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Connect to MySQL database
def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='anuradha',
        database='pythonclass'
    )

# Serve the HTML form
@app.route('/')
def form():
    return render_template('add_student_form.html')

# Create: Add a new student
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()  # Retrieve the JSON data from the request
    sid = data['sid']
    name = data['name']
    email = data['email']
    mobile = data['mobile']

    connection = get_db_connection()  # Establish connection to the database
    cursor = connection.cursor()  # Create a cursor to execute SQL queries
    insert_query = "INSERT INTO students (sid, name, email, mobile) VALUES (%s, %s, %s, %s)"  # Define SQL query
    cursor.execute(insert_query, (sid, name, email, mobile))  # Execute query with data

    connection.commit()  # Commit the transaction to the database
    cursor.close()  # Close the cursor
    connection.close()  # Close the connection

    return jsonify({'message': 'Student added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
