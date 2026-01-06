# Basil Backend

FastAPI backend service for the Basil multi-agent AI system.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Create a virtual environment** (recommended):

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   For Aspire integration with OpenTelemetry support:
   ```bash
   pip install -r requirements.txt -r requirements-aspire.txt
   ```

## Running the Backend

### Option 1: Using the startup script (recommended for Aspire)

The startup scripts automatically handle virtual environment activation:

```bash
# Windows
start.bat

# Linux/macOS
./start.sh
```

### Option 2: Manual execution

If you have activated your virtual environment:

```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using .NET Aspire

The backend is configured to run with .NET Aspire. Simply run the Aspire AppHost:

```bash
cd aspire/Basil.AppHost
dotnet run
```

The Aspire orchestrator will automatically start the backend using the startup script.

## Troubleshooting

### "No module named uvicorn" error

This error occurs when uvicorn is not installed in your Python environment. To fix:

1. **Ensure you have a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify uvicorn is installed**:
   ```bash
   python -m uvicorn --version
   ```

### Virtual environment not activating in Aspire

The startup scripts (`start.bat` and `start.sh`) will automatically detect and activate virtual environments in either `venv` or `.venv` directories. Make sure your virtual environment is created in the backend directory.

## API Documentation

Once running, visit:
- API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc
