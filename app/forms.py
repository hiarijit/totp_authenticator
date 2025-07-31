from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register') 

class VerifyForm(FlaskForm):
    token = StringField('TOTP Code', validators=[DataRequired()])
    submit = SubmitField('Verify Code')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


"""class ExternalVerifyForm(FlaskForm):
    token = StringField('TOTP Token', validators=[DataRequired()])
    submit = SubmitField('Verify')

    class Meta:
        csrf = False  # Disable CSRF just for this form

"""