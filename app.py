from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        # Using 'message' so the frontend finds the text
        return jsonify({'message': 'Email already exists'}), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_pw)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully!'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'message': 'A database error occurred. Please try again.'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    # Check if user exists AND if the password matches
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        # Standardized to 'message' with your specific text
        return jsonify({'message': 'wrong email or password, please try again'}), 401

    # Success case
    return jsonify({'message': f'Welcome back, {user.name}!'}), 200

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)