# Email Setup Guide for Portfolio Contact Form

## ✅ What's Been Implemented:
- Contact form now sends real emails to your Gmail address
- Form validation and error handling
- Success/error messages for users
- Secure environment variable configuration

## 🔧 Setup Required:

### 1. Get Gmail App Password
1. Go to your Google Account settings
2. Click "Security" in the left sidebar
3. Enable "2-Step Verification" if not already enabled
4. Go to "App passwords" section
5. Generate a new app password for "Mail"
6. Copy the 16-character password (it looks like: abcd efgh ijkl mnop)

### 2. Configure Environment Variables
Edit the file `/MacOS/.env` and replace `your_gmail_app_password_here` with your actual app password:

```
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

### 3. Test the Contact Form
1. Start your Django server: `python manage.py runserver`
2. Open the Contact app from your portfolio
3. Fill out and submit the form
4. Check your Gmail inbox for the message!

## 📧 How It Works:
- When someone submits the contact form, it sends an email to: `suchit.sharma.delhi@gmail.com`
- The email includes the sender's name, email, subject, and message
- The sender gets a success message on your portfolio
- You receive the full contact details in your inbox

## 🔒 Security Features:
- Gmail App Password (not your main password) 
- Environment variables (passwords not in code)
- CSRF protection on forms
- Input validation and sanitization

## 🛠️ Troubleshooting:
- If emails don't send: Check your app password in `.env`
- If forms show errors: Check Django logs in terminal
- Gmail blocks the app: Make sure 2-Step Verification is enabled

Your contact form is now fully functional! 🎉
