from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "donor" or "NGO"
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(50))   # Storing as string; convert to float if needed
    longitude = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
