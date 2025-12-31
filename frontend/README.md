# Basil UI - React Frontend

React-based web interface for the Basil Architecture Designer with Tailwind CSS.

## Features

- 📝 Interactive problem statement input form
- ⚙️ Advanced configuration options (LLM provider, cost optimization, etc.)
- 📊 Beautiful architecture visualization with Tailwind CSS
- 🤖 Detailed agent cards with specifications
- 💰 Cost estimation and analysis
- 🔀 Architecture graph visualization
- 📥 Export to multiple formats (JSON, YAML, Markdown, Mermaid)

## Quick Start

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
# Start development server (requires backend running on port 8000)
npm start
```

The app will open at http://localhost:3000

### Production Build

```bash
npm run build
```

## Backend Integration

The frontend expects a backend API running on port 8000. Start the backend first:

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

Then start the frontend in a separate terminal.
