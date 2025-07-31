from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
import pyotp
import qrcode
import io
import base64
from app.forms import RegisterForm, VerifyForm, LoginForm
from app.models import User
from app import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return redirect(url_for('main.register'))

        secret = pyotp.random_base32()
        user = User(username=username, secret=secret)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route('/qr')
def qr():
    username = session.get('username')
    if not username:
        flash("Please log in first.", "warning")
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('main.login'))

    # Generate provisioning URI for authenticator apps
    uri = pyotp.totp.TOTP(user.secret).provisioning_uri(name=user.username, issuer_name="MyTOTPApp")

    # Generate QR code image in memory
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    qr_data = base64.b64encode(buf.getvalue()).decode()

    return render_template('qr.html', qr_data=qr_data)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['username'] = user.username
            return redirect(url_for('main.qr'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)

@main.route('/verify', methods=['GET', 'POST'])
def verify():
    username = session.get('username')
    if not username:
        flash("Please log in first.")
        return redirect(url_for("main.login"))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for("main.login"))

    form = VerifyForm()

    if form.validate_on_submit():
        token = form.token.data
        totp = pyotp.TOTP(user.secret)
        if totp.verify(token):
            flash("Valid token!", "success")
        else:
            flash("Invalid token.", "danger")

    return render_template('verify.html', form=form)

"""

@main.route('/external_verify', methods=['GET', 'POST'])
def external_verify():
    username = request.args.get('user')
    if not username:
        return "Missing username", 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found", 404

    form = ExternalVerifyForm()
    if form.validate_on_submit():
        token = form.token.data
        totp = pyotp.TOTP(user.secret)
        if totp.verify(token):
            # Redirect back to password manager with 2FA success
            return redirect(f"http://localhost:5000/2fa_callback?2fa=true&user={username}")
        else:
            # Redirect back with failure
            return redirect(f"http://localhost:5000/2fa_callback?2fa=false&user={username}")

    return render_template('external_verify.html', form=form, username=username)

"""