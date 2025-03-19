from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = SelectField("Role", choices=[("donor", "Donor"), ("NGO", "NGO")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class DonationForm(FlaskForm):
    food_type = StringField("Food Type", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    expiry_date = DateTimeField("Expiry Date (YYYY-MM-DD HH:MM:SS)", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    location = StringField("Pickup Location", validators=[DataRequired()])
    latitude = HiddenField("Latitude")
    longitude = HiddenField("Longitude")
    submit = SubmitField("Donate")
class NGORegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    # Optionally use hidden fields with JavaScript geolocation:
    latitude = HiddenField("Latitude")
    longitude = HiddenField("Longitude")
    submit = SubmitField("Register")
