# Backend API

FastAPI service for AWS cost calculations and monitoring.

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Endpoints (planned)

- `GET /api/projects?budget=10` - Get affordable projects
- `GET /api/pricing/{service}` - Get current AWS pricing
- `POST /api/monitor` - Setup account monitoring (future)