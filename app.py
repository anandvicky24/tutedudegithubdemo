from flask import Flask, request, render_template, jsonify, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# MongoDB Atlas connection
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['flask_app']
users_collection = db['users']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        
        if not name or not email or not age:
            return render_template('form.html', error="All fields are required")
        
        user_data = {
            'name': name,
            'email': email,
            'age': int(age)
        }
        
        users_collection.insert_one(user_data)
        return redirect(url_for('success'))
    
    except Exception as e:
        return render_template('form.html', error=f"Error: {str(e)}")


@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)