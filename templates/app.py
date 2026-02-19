from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'tutedude_db')
COLLECTION_NAME = 'todo_items'

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    todo_collection = db[COLLECTION_NAME]
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"MongoDB connection error: {e}")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo')
def todo():
    """Render the To-Do page"""
    return render_template('todo.html')

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    """
    Backend API to accept and store To-Do items in MongoDB
    Expected JSON: {
        "itemName": "string",
        "itemDescription": "string"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        item_name = data.get('itemName', '').strip()
        item_description = data.get('itemDescription', '').strip()
        
        # Validate fields are not empty
        if not item_name:
            return jsonify({
                'success': False,
                'message': 'Item name is required'
            }), 400
        
        if not item_description:
            return jsonify({
                'success': False,
                'message': 'Item description is required'
            }), 400
        
        # Create document for MongoDB
        todo_document = {
            'itemName': item_name,
            'itemDescription': item_description,
            'createdAt': __import__('datetime').datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = todo_collection.insert_one(todo_document)
        
        return jsonify({
            'success': True,
            'message': 'To-Do item added successfully',
            'itemId': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        print(f"Error in submit_todo_item: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/gettodoitems', methods=['GET'])
def get_todo_items():
    """
    Retrieve all To-Do items from MongoDB
    """
    try:
        items = list(todo_collection.find({}, {'_id': 1, 'itemName': 1, 'itemDescription': 1, 'createdAt': 1}))
        
        # Convert ObjectId to string for JSON serialization
        for item in items:
            item['_id'] = str(item['_id'])
        
        return jsonify({
            'success': True,
            'items': items,
            'count': len(items)
        }), 200
    
    except Exception as e:
        print(f"Error in get_todo_items: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)