from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# example = {
#     "john_doe": {
#         {
#             "username": "testdriver",
#             "password": "testpass",
#             "role": "driver"
#         }
#     },
#     "route":{
#         "stops": ["Stop A", "Stop B", "Stop C", "Stop D"],
#         "timings": ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM"]
#    },
#    "classes":{
#        {
#             "className": "Physics",
#             "classTiming": "10:30"
#        }
#    }
# }

# mongodb_uri = "mongodb+srv://farjad19907:19907@cluster0.uaejnuk.mongodb.net/"
if mongodb_uri:
    client = MongoClient(mongodb_uri)
    db = client['bus']
    print("Connected to MongoDB through url" )
else:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bus']
    print("Connected to MongoDB through local host" )


# Serve frontend files
@app.route('/')
def serve_login():
    return send_from_directory('../Frontend', 'login.html')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory('../Frontend', path)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = db.users.find_one({'username': username, 'password': password, 'role': role})
    
    if user:
        # Check fee status for students
        if role == 'student' and user.get('fee_status') != 'paid':
            return jsonify({
                'message': 'Please pay your fee to access the system',
                'fee_status': 'unpaid'
            }), 403
            
        return jsonify({
            'message': 'Login successful',
            'user_id': str(user['_id']),
            'redirect': f'{role}_dashboard.html'
        })
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/students/<student_id>/classes', methods=['GET'])
def get_student_classes(student_id):
    student = db.users.find_one({'_id': ObjectId(student_id), 'role': 'student'})
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    classes = student.get('classes', [])
    return jsonify({'classes': classes})

@app.route('/students/<student_id>/classes', methods=['POST'])
def add_student_class(student_id):
    data = request.get_json()
    class_name = data.get('className')
    class_timing = data.get('classTiming')
    
    if not class_name or not class_timing:
        return jsonify({'error': 'Class name and timing are required'}), 400
    
    new_class = {
        'name': class_name,
        'timing': class_timing
    }
    
    result = db.users.update_one(
        {'_id': ObjectId(student_id)},
        {'$push': {'classes': new_class}}
    )
    
    if result.modified_count:
        return jsonify({'message': 'Class added successfully'})
    return jsonify({'error': 'Failed to add class'}), 500

@app.route('/routes/<driver_id>/stops', methods=['GET'])
def get_driver_routes(driver_id):
    try:
        driver = db.users.find_one({'_id': ObjectId(driver_id), 'role': 'driver'})
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404
        
        # Get route information from the routes collection
        route = db.routes.find_one({'driver_id': ObjectId(driver_id)})
        
        if not route:
            # If no route is assigned, return empty data
            return jsonify({
                'stops': [],
                'timings': []
            })
        
        return jsonify({
            'stops': route.get('stops', []),
            'timings': route.get('timings', [])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/users', methods=['GET'])
def get_all_users():
    users = list(db.users.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify({'users': users})

@app.route('/addUser', methods=['POST'])
def add_user():
    data = request.get_json()
    required_fields = ['username', 'password', 'role']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Username, password and role are required"}), 400

    username = data['username']
    password = data['password']
    role = data['role']

    # Check if the username already exists
    if db.users.find_one({'username': username}):
        return jsonify({"error": "Username already exists"}), 409

    # Add the new user with additional fields
    user_data = {
        "username": username,
        "password": password,
        "role": role,
        "classes": [] if role == 'student' else None,
        "routes": [] if role == 'driver' else None,
        "fee_status": "paid" if role == 'student' else None,  # New field for students
        "available_seats": 50 if role == 'driver' else None,  # New field for drivers
        "total_seats": 50 if role == 'driver' else None      # New field for drivers
    }
    
    result = db.users.insert_one(user_data)
    user_data['_id'] = str(result.inserted_id)

    return jsonify({
        "message": "User added successfully",
        "user_data": user_data
    }), 201

# Add a new endpoint to assign routes to drivers
@app.route('/routes/<driver_id>', methods=['POST'])
def assign_route(driver_id):
    try:
        data = request.get_json()
        if not data or 'stops' not in data or 'timings' not in data or 'coordinates' not in data:
            return jsonify({'error': 'Stops, timings, and coordinates are required'}), 400
            
        # Validate driver exists
        driver = db.users.find_one({'_id': ObjectId(driver_id), 'role': 'driver'})
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404
            
        # Update or insert route
        route_data = {
            'driver_id': ObjectId(driver_id),
            'stops': data['stops'],
            'timings': data['timings'],
            'coordinates': data['coordinates']  # Add coordinates
        }
        
        result = db.routes.update_one(
            {'driver_id': ObjectId(driver_id)},
            {'$set': route_data},
            upsert=True
        )
        
        return jsonify({'message': 'Route assigned successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/routes', methods=['GET'])
def get_all_routes():
    try:
        routes = list(db.routes.find())
        # Convert ObjectId to string for JSON serialization
        for route in routes:
            route['_id'] = str(route['_id'])
            route['driver_id'] = str(route['driver_id'])
        return jsonify({'routes': routes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add endpoint to update seat availability
@app.route('/drivers/<driver_id>/seats', methods=['PUT'])
def update_seats(driver_id):
    try:
        data = request.get_json()
        available_seats = data.get('available_seats')
        
        if available_seats is None:
            return jsonify({'error': 'Available seats count is required'}), 400
            
        result = db.users.update_one(
            {'_id': ObjectId(driver_id), 'role': 'driver'},
            {'$set': {'available_seats': available_seats}}
        )
        
        if result.modified_count:
            return jsonify({'message': 'Seats updated successfully'})
        return jsonify({'error': 'Driver not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add endpoint to update student fee status
@app.route('/students/<student_id>/fee', methods=['PUT'])
def update_fee_status(student_id):
    try:
        data = request.get_json()
        fee_status = data.get('fee_status')
        
        if fee_status not in ['paid', 'unpaid']:
            return jsonify({'error': 'Invalid fee status'}), 400
            
        result = db.users.update_one(
            {'_id': ObjectId(student_id), 'role': 'student'},
            {'$set': {'fee_status': fee_status}}
        )
        
        if result.modified_count:
            return jsonify({'message': 'Fee status updated successfully'})
        return jsonify({'error': 'Student not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add endpoint to get seat availability
@app.route('/drivers/<driver_id>/seats', methods=['GET'])
def get_seats(driver_id):
    try:
        driver = db.users.find_one({'_id': ObjectId(driver_id), 'role': 'driver'})
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404
            
        return jsonify({
            'available_seats': driver.get('available_seats', 0),
            'total_seats': driver.get('total_seats', 50)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
