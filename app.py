from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
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
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Wrong email or password, please try again'}), 401
    session['user_id'] = user.id
    session['mode'] = 'customer'
    return jsonify({'message': f'Welcome back, {user.name}!'}), 200

@app.route('/switch-mode')
def switch_mode():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    session['mode'] = 'customer' if session.get('mode') == 'cook' else 'cook'
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/check-profile')
def check_profile():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('profile.html')  # empty for now

@app.route('/check-order')
def check_order():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return redirect('/menu')

@app.route('/login-page')
def login_page():
    return render_template('login.html')
@app.route('/check-session')
def check_session():
    return jsonify({'logged_in': 'user_id' in session})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)