# Running Basil with UI

This guide shows you how to run Basil with the React web interface.

## Architecture

```
┌─────────────────────┐
│   React Frontend    │
│   (Port 3000)       │
│   - Tailwind CSS    │
│   - Form inputs     │
│   - Visualizations  │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│   FastAPI Backend   │
│   (Port 8000)       │
│   - REST API        │
│   - Basil framework │
└─────────────────────┘
```

## Method 1: Manual Setup (Recommended for Development)

### Step 1: Start the Backend

```bash
# From project root
cd backend
pip install -r requirements.txt
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

### Step 2: Start the Frontend

In a new terminal:

```bash
# From project root
cd frontend
npm install
npm start
```

Frontend will open automatically at http://localhost:3000

## Method 2: Docker Compose (Production)

```bash
# From project root
docker-compose up --build
```

This starts both frontend and backend:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Using the Web UI

### 1. Input Problem Statement

Enter your application requirements in the problem statement textarea. Be specific:

**Example:**
```
Build an e-commerce platform with:
- User authentication (OAuth, email/password)
- Product catalog with search and filtering
- Shopping cart and checkout
- Payment processing (Stripe integration)
- Inventory management
- Order tracking
- Email notifications
- Admin dashboard with analytics
```

### 2. Configure Options

**LLM Provider Preference:**
- Auto: Basil chooses based on task
- OpenAI: Prefer GPT models
- Anthropic: Prefer Claude models

**Cost Optimize:**
- ✅ Enabled: Use cheaper models when possible
- ❌ Disabled: Prioritize performance

**Max Agents:** Optional limit on number of agents (1-20)

**Complexity Preference:**
- Low: Simpler, cheaper agents
- Medium: Balanced
- High: More powerful, expensive agents

### 3. Design Architecture

Click "🚀 Design Architecture" to generate your multi-agent design.

### 4. View Results

The UI provides multiple tabs:

**Overview Tab:**
- Quick statistics
- Agent distribution
- LLM distribution
- Validation status

**Agents Tab:**
- Detailed agent cards
- Capabilities and dependencies
- LLM assignments
- Reusability scores

**Architecture Graph Tab:**
- Visual communication flows
- Agent relationships
- Mermaid diagram code

**Cost Analysis Tab:**
- Monthly cost estimates (10K, 100K, 1M requests)
- Per-agent breakdown
- Cost by LLM tier
- Optimization tips

**Raw Data Tab:**
- Complete JSON output
- Copy-paste friendly

### 5. Export Architecture

Click "📥 Export" to download in various formats:
- JSON
- YAML
- Markdown (documentation)
- Mermaid (diagrams)

## Input Fields Reference

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| Problem Statement | Detailed description of your application | "Build a customer service platform with..." |

### Optional Configuration

| Field | Options | Default | Impact |
|-------|---------|---------|--------|
| LLM Provider | Auto, OpenAI, Anthropic | Auto | Which models to prefer |
| Cost Optimize | On/Off | Off | Use cheaper models when possible |
| Max Agents | 1-20 | Auto | Limit number of agents |
| Complexity | Low/Medium/High | Auto | Agent sophistication level |

## Tips for Best Results

### ✅ Do:
- Be specific about features and integrations
- Mention scale requirements (users, requests/sec)
- Include technical constraints (compliance, security)
- List all major functionalities
- Specify external services (Stripe, AWS, etc.)

### ❌ Don't:
- Write vague descriptions like "build an app"
- Skip important features
- Use overly technical jargon without context

## Examples

### Example 1: E-commerce Platform
```
Problem Statement:
Build an e-commerce platform with user authentication,
product catalog (10K+ products), shopping cart, payment
processing (Stripe), inventory management, order tracking,
and ML-based product recommendations.

Config:
- Provider: Anthropic
- Cost Optimize: Yes
- Max Agents: 8
```

Result: 6-8 agents with mix of Claude Haiku (API, cart) and Sonnet (recommendations, coordination)

### Example 2: Data Pipeline
```
Problem Statement:
Design a data processing pipeline for financial analytics.
Ingest data from APIs and databases, perform ETL
transformations, validate data quality, run ML inference
for predictions, store in PostgreSQL, and generate
real-time dashboards.

Config:
- Provider: OpenAI
- Cost Optimize: No
- Complexity: High
```

Result: 5-7 agents with GPT-4 for ML tasks, GPT-3.5 for ETL

### Example 3: Customer Service Bot
```
Problem Statement:
Create a customer service system with intent classification,
FAQ answering from knowledge base, ticket creation in Zendesk,
sentiment analysis, and automated email responses.

Config:
- Provider: Auto
- Cost Optimize: Yes
```

Result: 4-5 agents, mostly efficient models (GPT-3.5, Claude Haiku)

## Troubleshooting

### Backend Not Connecting
```bash
# Check if backend is running
curl http://localhost:8000

# Should return: {"status":"healthy",...}
```

### CORS Errors
The backend is configured to allow all origins in development. In production, update `backend/api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    ...
)
```

### Port Already in Use
```bash
# Backend (change port 8000)
uvicorn backend.api:app --port 8001

# Frontend (change port 3000 in package.json)
PORT=3001 npm start
```

## API Endpoints

The backend exposes these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/models` | GET | List available LLM models |
| `/api/domains` | GET | List supported domains |
| `/api/agent-types` | GET | List agent types |
| `/api/design` | POST | Design architecture |
| `/api/export` | POST | Export architecture |

## Environment Variables

### Backend
```bash
# Optional: API keys for LLM providers
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

### Frontend
```bash
# API URL (for production builds)
REACT_APP_API_URL=https://api.your-domain.com
```

## Production Deployment

### Backend
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn backend.api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
# Build optimized production bundle
npm run build

# Serve with nginx or any static file server
```

## Next Steps

1. Try the quick start examples in the UI
2. Experiment with different configurations
3. Export your favorite architectures
4. Use exported designs to implement with Semantic Kernel, LangChain, etc.

Happy architecting! 🚀
