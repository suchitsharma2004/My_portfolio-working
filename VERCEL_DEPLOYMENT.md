# Vercel Deployment Guide for Django Portfolio

This guide will help you deploy your Django portfolio project to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Environment Variables**: Prepare your production environment variables

## Files Created for Deployment

- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel configuration
- `production_settings.py` - Production Django settings
- `.env.example` - Example environment variables
- `build.sh` - Build script (optional)

## Step-by-Step Deployment

### 1. Push to GitHub

Make sure all your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and log in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it as a Python project

### 3. Configure Environment Variables

In your Vercel dashboard, go to Settings > Environment Variables and add:

- `SECRET_KEY`: Your Django secret key
- `EMAIL_HOST_PASSWORD`: Your Gmail app password
- `VERCEL`: Set to `1` (this tells the app to use production settings)

### 4. Deploy

Click "Deploy" and Vercel will:
- Install dependencies from `requirements.txt`
- Build your Django application
- Deploy it to a Vercel URL

## Important Notes

### Database
- Currently configured to use SQLite (simple but not ideal for production)
- For production, consider using PostgreSQL with Vercel's database add-ons

### Static Files
- Configured to use WhiteNoise for serving static files
- Static files are collected during the build process

### Security
- Debug mode is disabled in production
- HTTPS redirects are enabled
- Security headers are configured

### Custom Domain
To use a custom domain:
1. Add your domain in Vercel dashboard
2. Update `ALLOWED_HOSTS` in `production_settings.py`
3. Update `CSRF_TRUSTED_ORIGINS` accordingly

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Static Files Not Loading**: Check if `collectstatic` ran successfully
3. **CSRF Errors**: Ensure your domain is in `CSRF_TRUSTED_ORIGINS`

### Viewing Logs
- Check Vercel function logs in the dashboard
- Use `vercel logs [deployment-url]` in CLI

### Local Testing with Production Settings
```bash
export VERCEL=1
python manage.py runserver
```

## Post-Deployment

1. Test all functionality on the deployed site
2. Check that forms work correctly
3. Verify email functionality
4. Test responsive design

## Environment Variables Reference

Create these in Vercel dashboard:

```
SECRET_KEY=your-django-secret-key
EMAIL_HOST_PASSWORD=your-gmail-app-password
VERCEL=1
```

## Next Steps

1. Set up a custom domain
2. Configure a production database (PostgreSQL)
3. Set up monitoring and analytics
4. Configure backup strategies

---

**Need Help?**
- Check Vercel documentation: https://vercel.com/docs
- Django deployment guide: https://docs.djangoproject.com/en/stable/howto/deployment/
