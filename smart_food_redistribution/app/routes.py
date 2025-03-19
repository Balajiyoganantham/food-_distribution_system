from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app import db, bcrypt, mail
from app.models import User, Donation
from app.forms import RegistrationForm, LoginForm, DonationForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
import requests

main = Blueprint('main', __name__)

# def send_donation_email(donation):
#     """
#     Sends an email with donation details including the captured latitude and longitude
#     to the donor.
#     """
#     msg = Message("Donation Confirmation",
#                   recipients=[current_user.email])
#     msg.body = (f"Thank you for your donation!\n\n"
#                 f"Food Type: {donation.food_type}\n"
#                 f"Quantity: {donation.quantity}\n"
#                 f"Expiry Date: {donation.expiry_date}\n"
#                 f"Pickup Location: {donation.location}\n"
#                 f"Coordinates: (Lat: {donation.latitude}, Lon: {donation.longitude})\n")
#     mail.send(msg)
def send_donation_email(donation):
    try:
        msg = Message("Donation Confirmation",
                      recipients=[current_user.email])
        msg.body = (
            f"Thank you for your donation!\n\n"
            f"Food Type: {donation.food_type}\n"
            f"Quantity: {donation.quantity}\n"
            f"Expiry Date: {donation.expiry_date}\n"
            f"Pickup Location: {donation.location}\n"
            f"Coordinates: (Lat: {donation.latitude}, Lon: {donation.longitude})\n"
        )
        print("DEBUG: Sending email to:", current_user.email)
        mail.send(msg)
        print("DEBUG: Email sent successfully.")
    except Exception as e:
        print("DEBUG: Error sending email:", e)


def send_ngo_notification_email(ngo, donation):
    """
    Sends an email notification to the nearest NGO with the donation details.
    """
    if not ngo:
        return  # No NGO found to notify.
    msg = Message("New Donation Available",
                  recipients=[ngo.email])
    msg.body = (f"Dear {ngo.name},\n\n"
                f"A new donation is available nearby!\n\n"
                f"Donation Details:\n"
                f"Food Type: {donation.food_type}\n"
                f"Quantity: {donation.quantity}\n"
                f"Expiry Date: {donation.expiry_date}\n"
                f"Pickup Location: {donation.location}\n"
                f"Coordinates: (Lat: {donation.latitude}, Lon: {donation.longitude})\n\n"
                f"Please log in to your dashboard for more details.\n\n"
                f"Thank you,\n"
                f"Smart Food Redistribution System")
    mail.send(msg)
LARGE_QUANTITY_THRESHOLD = 100  # Example threshold; adjust as needed
NEARBY_RADIUS_KM = 10           # Notify NGOs within 10 km for large donations

from app.matching import calculate_distance

def notify_ngos_about_donation(donation, ngo_list):
    """
    Notifies NGOs based on the donation's quantity.
    If quantity is large, notify all NGOs within NEARBY_RADIUS_KM.
    Otherwise, notify only the nearest NGO.
    """
    try:
        d_lat = float(donation.latitude)
        d_lon = float(donation.longitude)
    except (TypeError, ValueError):
        return

    if donation.quantity >= LARGE_QUANTITY_THRESHOLD:
        # Notify all NGOs within the specified radius.
        for ngo in ngo_list:
            if ngo.latitude and ngo.longitude:
                try:
                    n_lat = float(ngo.latitude)
                    n_lon = float(ngo.longitude)
                    distance = calculate_distance(d_lat, d_lon, n_lat, n_lon)
                    if distance <= NEARBY_RADIUS_KM:
                        send_ngo_notification_email(ngo, donation)
                except (TypeError, ValueError):
                    continue
    else:
        # Notify only the nearest NGO.
        from app.matching import get_nearest_ngo
        nearest_ngo = get_nearest_ngo(donation, ngo_list)
        send_ngo_notification_email(nearest_ngo, donation)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=hashed_pw,
                    role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)
from datetime import datetime


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Login failed. Please check your credentials.", "danger")
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == "donor":
        donations = Donation.query.filter_by(donor_id=current_user.id).all()
    else:
        donations = Donation.query.all()
    return render_template('dashboard.html', donations=donations)
@main.route('/donate_food', methods=['GET', 'POST'])
@login_required
def donate_food():
    form = DonationForm()
    if form.validate_on_submit():
        try:
            donation = Donation(
                donor_id=current_user.id,
                food_type=form.food_type.data,
                quantity=form.quantity.data,
                expiry_date=form.expiry_date.data,
                location=form.location.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data
            )
            db.session.add(donation)
            db.session.commit()
            # Send confirmation email to donor
            send_donation_email(donation)
            
            # Fetch NGO list (NGOs must have location info stored)
            ngo_list = User.query.filter_by(role="NGO").all()
            # Notify NGOs based on donation quantity and proximity
            notify_ngos_about_donation(donation, ngo_list)
            
            flash("Food Donation Successful! Confirmation email sent and NGOs notified as appropriate.", "success")
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while donating food: " + str(e), "danger")
    return render_template('donate_food.html', form=form)

from datetime import datetime

@main.route("/food_list")
def food_list():
    current_time = datetime.now()
    
    # Fetch donations from database
    donations = Donation.query.all()

    # Sort donations:
    # 1. Highest quantity first
    # 2. Expired food at the bottom
    donations = sorted(donations, key=lambda x: (x.expiry_date < current_time, -x.quantity))

    return render_template("food_list.html", donations=donations, current_time=current_time)

@main.route('/geocode', methods=['GET'])
def geocode():
    # This endpoint demonstrates calling an external API to convert an address to coordinates.
    address = request.args.get('address')
    if not address:
        return {"error": "Address parameter is missing."}, 400

    api_key = current_app.config.get("GOOGLE_MAPS_API_KEY")
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_url).json()
    return response

