from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  email = StringField("email", validators=[DataRequired()])
  senha = PasswordField("senha", validators=[DataRequired()])
  lembrar = BooleanField("lembrar")