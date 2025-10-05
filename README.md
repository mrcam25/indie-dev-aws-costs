# Indie Dev AWS Costs

Budget planning tool for indie developers to manage AWS infrastructure costs.

## Project Structure

```
indie-dev-aws-costs/
├── frontend/          # React + Vite
├── backend/           # FastAPI + boto3
└── README.md
```

## Setup

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Current Status

- Frontend MVP - Budget calculator with project templates
- Backend API - In progress
- AWS pricing integration - Planned
- User account monitoring - Planned
