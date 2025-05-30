# Attendia Server

Backend for Attendia app. Built with Flask + SQLAlchemy.

## 🚀 Quickstart on Render

1. Fork this repo or upload your own
2. Go to https://render.com
3. Create New Web Service → Connect your GitHub repo
4. Set the build/start command: `gunicorn app:app`
5. Set environment variables:
   - `SECRET_KEY=your_secret`
   - `DATABASE_URL=sqlite:///attendia.db` or your MySQL URI

## API Endpoints

- POST `/register`
- POST `/login`
- POST `/sync`
- GET `/pull`
