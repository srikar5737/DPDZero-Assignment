from flask import Flask, request, jsonify , send_from_directory , abort , session 
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(seconds=3600)
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Data model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Data {self.key}>'

# Move the creation of the database tables within the application context
with app.app_context():
    db.create_all()

# User Registration API
@app.route('/')
def serve_index():
    # print(os.getcwd())
    return send_from_directory('./frontend', 'index.html')
@app.route('/registration')
def registration():
    # print(os.getcwd())
    return send_from_directory('./frontend', 'registration.html')
@app.route('/edit_data')
def edit_data():
    # print(os.getcwd())
    return send_from_directory('./frontend', 'edit_data.html')
@app.route('/generate_token')
def generate():
    # print(os.getcwd())
    return send_from_directory('./frontend', 'generate_token.html')
@app.route('/retrieve_data')
def retieve_data():
    # print(os.getcwd())
    return send_from_directory('./frontend', 'retrieve_data.html')
@app.route('/store_data')
def store():
    # print(os.getcwd())
    return send_from_directory('./frontend', 'store_data.html')
@app.route('/delete_data')
def delete():
    # print(os.getcwd())
    return send_from_directory('./frontend', 'delete_data.html')

@app.route('/api/register', methods=['POST'])
def user_registration():
    data = request.json

    # Validate required fields
    required_fields = ['username', 'email', 'password', 'full_name']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "status": "error",
                "code": "INVALID_REQUEST",
                "message": f"Invalid request. Please provide all required fields: {', '.join(required_fields)}."
            }), 400

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            "status": "error",
            "code": "USERNAME_EXISTS",
            "message": "The provided username is already taken. Please choose a different username."
        }), 409

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            "status": "error",
            "code": "EMAIL_EXISTS",
            "message": "The provided email is already registered. Please use a different email address."
        }), 409
    #Validating Password
    password = data["password"]
    if not (len(password) >= 8 and any(char.isupper() for char in password) and any(char.islower() for char in password) and any(char.isdigit() for char in password) and any(not char.isalnum() for char in password)):
        return jsonify(status="error", code="INVALID_PASSWORD", message="The provided password does not meet the requirements. Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters.")

    # Store user data in the database
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        full_name=data['full_name'],
        age=data.get('age'),
        gender=data['gender']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User successfully registered!",
        "data": {
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "age": new_user.age,
            "gender": new_user.gender
        }
    }), 201

# Generate Token API
@app.route('/api/token', methods=['POST'])
def generate_token():
    data = request.json
    # print(request.json)

    # Check if both username and password are provided
    if 'username' not in data or 'password' not in data:
        return jsonify({
            "status": "error",
            "code": "MISSING_FIELDS",
            "message": "Missing fields. Please provide both username and password."
        }), 400

    # Check if username exists and validate password
    user = User.query.filter_by(username=data['username']).first()
    if not user or user.password != data['password']:
        return jsonify({
            "status": "error",
            "code": "INVALID_CREDENTIALS",
            "message": "Invalid credentials. The provided username or password is incorrect."
        }), 401

    # Generate and return a dummy access token
    access_token = "SAMPLE_ACCESS_TOKEN"
    expires_in = 3600
    session['access_token'] = "<YOUR_GENERATED_ACCESS_TOKEN>"
    return jsonify({
        "status": "success",
        "message": "Access token generated successfully.",
        "data": {
            "access_token": access_token,
            "expires_in": expires_in
        }
    }), 200

# Store Data API
@app.route('/api/data', methods=['POST'])
def store_data():
    data = request.json
    print(request.json)
    access_token =get_access_token()
    if not access_token :
        abort(401, "Unauthorized")

    # Validate required fields
    if 'key' not in data:
        return jsonify({
            "status": "error",
            "code": "INVALID_KEY",
            "message": "The provided key is not valid or missing."
        }), 400

    if 'value' not in data:
        return jsonify({
            "status": "error",
            "code": "INVALID_VALUE",
            "message": "The provided value is not valid or missing."
        }), 400

    # Check if the key already exists
    if Data.query.filter_by(key=data['key']).first():
        return jsonify({
            "status": "error",
            "code": "KEY_EXISTS",
            "message": "The provided key already exists in the database. To update an existing key, use the update API."
        }), 409

    # Store the data in the database
    new_data = Data(
        key=data['key'],
        value=data['value']
    )

    db.session.add(new_data)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Data stored successfully."
    }), 201

# Retrieve Data API
@app.route('/api/data/<string:key>', methods=['GET'])
def retrieve_data(key):
    # Check if the key exists
    data = Data.query.filter_by(key=key).first()
    access_token = get_access_token()
    if not access_token :
        abort(401, "Unauthorized")

    if not data:
        return jsonify({
            "status": "error",
            "code": "KEY_NOT_FOUND",
            "message": "The provided key does not exist in the database."
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "key": data.key,
            "value": data.value
        }
    }), 200

# Update Data API
@app.route('/api/data/<string:key>', methods=['PUT'])
def update_data(key):
    data = request.json
    access_token = get_access_token()
    if not access_token :
        abort(401, "Unauthorized")


    # Check if the key exists
    existing_data = Data.query.filter_by(key=key).first()
    if not existing_data:
        return jsonify({
            "status": "error",
            "code": "KEY_NOT_FOUND",
            "message": "The provided key does not exist in the database."
        }), 404

    # Update the value if provided
    if 'value' in data:
        existing_data.value = data['value']

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Data updated successfully."
    }), 200

# Delete Data API
@app.route('/api/data/<string:key>', methods=['DELETE'])
def delete_data(key):
    # Check if the key exists
    existing_data = Data.query.filter_by(key=key).first()
    access_token = get_access_token()
    if not access_token :
        abort(401, "Unauthorized")

    if not existing_data:
        return jsonify({
            "status": "error",
            "code": "KEY_NOT_FOUND",
            "message": "The provided key does not exist in the database."
        }), 404

    # Delete the data from the database
    db.session.delete(existing_data)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Data deleted successfully."
    }), 200
@app.route('/logout')
def logout():
    session.clear()
    return jsonify(status="success", message="Logout successful.")


def get_access_token():
    return  session.get('access_token')

if __name__ == '__main__':
    app.run(debug=True)
