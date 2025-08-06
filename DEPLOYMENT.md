# Deployment Guide

## 🚀 Deploy to Vercel

### Prerequisites:
1. Gmail App Password configured
2. Environment variables set in Vercel

### Vercel Environment Variables:
Add these in your Vercel project settings:

```
EMAIL_HOST_PASSWORD=your_gmail_app_password_here
DEBUG=False
SECRET_KEY=your_production_secret_key_here
```

### Local Development:
1. Copy `.env.example` to `.env`
2. Fill in your actual credentials
3. Never commit `.env` to git

### Security Notes:
- ✅ `.env` is in `.gitignore`
- ✅ Use `.env.example` for documentation
- ✅ Set environment variables in Vercel dashboard
- ✅ Use different SECRET_KEY for production

### Gmail Setup:
1. Enable 2-Step Verification
2. Generate App Password for Mail
3. Use 16-character app password (not your Gmail password)

## 📧 Email Configuration:
- Development: Uses local .env file
- Production: Uses Vercel environment variables
- Emails sent to: suchit.sharma.delhi@gmail.com
