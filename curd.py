from flask import Flask, request, jsonify, render_template
import pymysql
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    return render_template('crud_oper.html')

# Create: Add a new student
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json() # Retrieve the JSON data sent in the request body
    sid = data['sid'] # Extract the 'sid' field from the JSON data and assign it to the variable 'sid' and go on
    name = data['name']
    email = data['email']
    mobile = data['mobile']
    
    connection = get_db_connection() # Establish a connection to the database
    cursor = connection.cursor() # Create a cursor object to execute SQL queries
    insert_query = "INSERT INTO students (sid, name, email, mobile) VALUES (%s, %s, %s, %s)"  ##Define the SQL query to insert data into the 'students' table .#%s is a placeholder for the actual values that will be provided when the query is executed.
    cursor.execute(insert_query, (sid, name, email, mobile)) # Execute the SQL query with provided values (sid, name, email, mobile)                                
    connection.commit() # Commit the transaction to save the changes in the database
    cursor.close() # Close the cursor to free up resources
    connection.close() # Close the connection to the database

    return jsonify({'message': 'Student added successfully'})


# Read: Get a student by ID
@app.route('/student/<int:sid>', methods=['GET'])
def get_student(sid):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        select_query = "SELECT * FROM students WHERE sid = %s"
        cursor.execute(select_query, (sid,))
        student = cursor.fetchone()
        
        cursor.close()
        connection.close()

        if student:
            return jsonify(student), 200  # Successful response with student data
        else:
            return jsonify({'message': 'Student not found'}), 404  # Student not found
        
    except Exception as e:
        # Log the exception (optional) and return a generic error message
        print(f"Error: {e}")  # For debugging purposes, you can remove this line in production
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500  # Internal Server Error


# Update: Update student information
@app.route('/student/<int:sid>', methods=['PUT'])
def update_student(sid):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    mobile = data.get('mobile')

    connection = get_db_connection()
    cursor = connection.cursor()
    update_query = """
        UPDATE students
        SET name = %s, email = %s, mobile = %s
        WHERE sid = %s
    """
    cursor.execute(update_query, (name, email, mobile, sid))
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        return jsonify({'message': 'Student updated successfully'})
    else:
        return jsonify({'message': 'Student not found'})

# Delete: Delete a student by ID
@app.route('/student/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    connection = get_db_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM students WHERE sid = %s"
    cursor.execute(delete_query, (sid,))
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0: #If the condition is true (i.e., at least one row was deleted), this line returns a JSON response with a message saying "Student deleted successfully".This checks if the number of rows affected by the previous SQL operation (such as a DELETE statement) is greater than zero. If so, it means that at least one row was successfully deleted.
        return jsonify({'message': 'Student deleted successfully'})
    else:
        return jsonify({'message': 'Student not found'})

if __name__ == '__main__':
    app.run(debug=True)



















   # run
# python CURD.py at terminal 

# and then performe CURD operation

# 1.create(Push)
   # http://127.0.0.1:5000/student/20/chhoti /chhoti@example.com/1234567890

# 2.Read(get)
 # read all quries
 # read where sid = 20

# Update(put)
# update sid 2 to 22

# delete(DELETE )
  # delete sid :20
