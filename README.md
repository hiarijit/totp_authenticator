# 📱 TOTP Authenticator

This is a standalone Flask-based TOTP (Time-based One-Time Password) Authenticator app. It allows users to register, generate TOTP secrets, and verify codes. It is designed to integrate with external applications (like a password manager) via a secure redirect-based flow.

## ✨ Features

✅ User registration and login
🔐 TOTP-based two-factor authentication (2FA)
📱 QR code generation for use with apps like Google Authenticator or Authy
🌐 Redirect-based verification support for integration with other applications
💾 SQLite database support

## 🛠️ Technologies Used

Flask
Flask-Login
Flask-WTF
PyOTP
qrcode
SQLite

## 🚀 Setup Instructions

```bash
1. Clone the Repository
git clone https://github.com/yourusername/totp-authenticator.git
cd totp-authenticator

2. Create and Activate Virtual Environment
python -m venv env

\# For Windows:
env\Scripts\activate
\# For Linux/Mac:
source env/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Create .env File
SECRET_KEY=your_secret_key_here

5. Run the App
python run.py

The application will start at http://localhost:5000.
```

## 🔄 External App Integration
You can integrate this TOTP app into other applications using a redirect-based approach:

```bash
http://localhost:5000/verify?username=someuser&redirect_url=http://localhost:5001/2fa_callback
```
username: The user to verify

redirect_url: External app endpoint to redirect back with ?status=success or ?status=failure

## 🔒 Security Notes
Always use HTTPS in production.

Keep SECRET_KEY and TOTP secrets confidential.

This app should be hosted securely and only trusted applications should be allowed to use its verification service.

## 📄 License
This project is licensed under the MIT License.

