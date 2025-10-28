# Indie Dev AWS Costs

Budget planning tool for indie developers to manage AWS infrastructure costs. Discover what you can build and deploy on AWS within your budget.

## Project Goal

Help indie developers and learners practice AWS deployment without financial anxiety. Answer the question: "I have $10/month - what can I actually build?"

## Features

- Interactive budget calculator
- 6+ pre-configured project templates with detailed cost breakdowns
- Real-time filtering based on budget
- Complexity indicators (Beginner/Intermediate/Advanced)
- RESTful API backend with FastAPI
- Modern React frontend with Tailwind CSS
- Live AWS pricing integration (coming soon)
- AWS account monitoring (planned)

## Project Structure

```
indie-dev-aws-costs/
├── frontend/          # React + Vite + Tailwind
│   ├── src/
│   │   ├── App.jsx    # Main calculator component
│   │   ├── main.jsx   # React entry point
│   │   └── index.css  # Tailwind imports
│   └── package.json
├── backend/           # FastAPI + boto3
│   ├── app/
│   │   ├── main.py       # FastAPI app with CORS
│   │   └── projects.py   # Project templates & logic
│   └── requirements.txt
└── README.md
```

## Setup & Installation

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- npm or yarn

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: http://localhost:5173

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on: http://127.0.0.1:8000

API docs available at: http://127.0.0.1:8000/docs

## API Endpoints

- `GET /` - Health check
- `GET /api/projects?budget={amount}` - Get projects within budget
- `GET /api/projects/all` - Get all project templates
- `GET /api/health` - Detailed health check
- `GET /docs` - Interactive API documentation (Swagger UI)

### Example API Usage

```bash
# Get projects for $10 budget
curl "http://127.0.0.1:8000/api/projects?budget=10"

# Get all projects
curl "http://127.0.0.1:8000/api/projects/all"
```

## Learning Objectives

This project helps practice:
- **React**: hooks (useState, useEffect), component composition, props
- **Python**: FastAPI, Pydantic models, type hints
- **APIs**: RESTful design, CORS, query parameters
- **Full-stack**: connecting frontend to backend
- **AWS**: boto3 SDK, pricing APIs (coming soon)

## Roadmap

### Phase 1: MVP
- [x] React frontend with budget calculator
- [x] FastAPI backend with project templates
- [x] Frontend-backend integration
- [x] Interactive API documentation

### Phase 2: Real Data (In Progress)
- [ ] Integrate AWS Price List API
- [ ] Dynamic cost calculations
- [ ] Multi-region pricing support

### Phase 3: User Features (Planned)
- [ ] AWS account monitoring
- [ ] Budget alerts
- [ ] Cost optimization recommendations
- [ ] Save/export project plans

### Phase 4: Deployment (Planned)
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Railway/Render
- [ ] Add authentication
- [ ] Production database

## Development

### Running Both Services

**Terminal 1 (Backend):**
```bash
cd backend && source venv/bin/activate && uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm run dev
```

### Testing the API
Visit http://127.0.0.1:8000/docs for interactive API testing with Swagger UI.

## Tech Stack

**Frontend:**
- React 18
- Vite (build tool)
- Tailwind CSS
- Fetch API

**Backend:**
- FastAPI
- Pydantic (data validation)
- Uvicorn (ASGI server)
- boto3 (AWS SDK - coming soon)

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contributing

This is a learning project, but suggestions and improvements are welcome! Feel free to open issues or submit PRs.

## Project Templates Included

1. **Static Portfolio Website** - $1.50/month
2. **Serverless REST API** - $4.50/month
3. **Scheduled Data Scraper** - $2.00/month
4. **Small Full-Stack App** - $9.50/month
5. **Image Processing Service** - $3.50/month
6. **Discord/Slack Bot** - $1.00/month

All templates include detailed AWS service breakdowns and estimated traffic handling.

---

Built with ☕ while learning React and Python