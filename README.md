# Gym Management System

A full-stack gym management app. Login works, dashboard loads, UI is there.

## What It Does

- Admin login system
- Dashboard with stats
- Member management
- Memberships, payments, attendance tracking
- Basic gym operations

## Tech

FastAPI, React, SQLite, Tailwind CSS

## Setup

### Backend

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload


### Frontend

cd frontend
npm install
npm run dev


## Login

Email: `admin@gym.com`  
Password: `admin123`

## Project Structure

backend/
├── app/models/
├── app/routers/
├── app/schemas/
└── main.py

frontend/
├── src/pages/
├── src/components/
├── src/context/
└── App.jsx


## What Works

✅ Login & auth  
✅ Dashboard loads  
✅ Page routing  
✅ Database connection

## What Needs Work

- Dashboard buttons not connected
- Some UI components are placeholders
- Backend endpoints partially integrated
- Forms need full implementation

---

**Author:** Surya Pratap Singh  
**GitHub:** [@FAKE-SURYA](https://github.com/FAKE-SURYA)
