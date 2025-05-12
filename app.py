from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

DATABASE = 'sql_murder_mystery.db'

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database if it doesn't exist
def init_db():
    """Initialize the database with schema and data if it doesn't exist"""
    if os.path.exists(DATABASE):
        print(f"Database {DATABASE} already exists")
        return
    
    print(f"Creating new database: {DATABASE}")
    
    # Create a new database connection
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    # Execute schema.sql to create tables
    try:
        with open('database/schema.sql', 'r') as f:
            schema_script = f.read()
        cursor.executescript(schema_script)
        print("Schema created successfully")
    except Exception as e:
        print(f"Error creating schema: {e}")
        connection.close()
        return
    
    # Execute data.sql to populate tables
    try:
        with open('database/data.sql', 'r') as f:
            data_script = f.read()
        cursor.executescript(data_script)
        connection.commit()
        print("Data imported successfully")
    except Exception as e:
        print(f"Error importing data: {e}")
    
    connection.close()

# API endpoint to execute player SQL queries
@app.route('/api/execute-query', methods=['POST'])
def execute_query():
    data = request.get_json()
    query = data.get('query', '')

    # Basic validation: only allow SELECT queries
    if not query.strip().lower().startswith('select'):
        return jsonify({'error': 'Only SELECT queries are allowed.'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API endpoint to check the player's solution
@app.route('/api/check-solution', methods=['POST'])
def check_solution():
    data = request.get_json()
    murderer_id = data.get('murdererId')

    # The actual murderer is Laura White with PersonID 6
    if murderer_id == 6 or murderer_id == '6':
        return jsonify({'correct': True, 'message': 'Congratulations! You have solved the case! Laura White is indeed the murderer. She killed John Smith to prevent him from exposing her journalistic fraud.'}), 200
    else:
        return jsonify({'correct': False, 'message': 'Incorrect. Your Career as a Detective is as dead as the Victim.'}), 200

if __name__ == '__main__':
    init_db()  # Initialize database if it doesn't exist
    app.run(debug=True)
