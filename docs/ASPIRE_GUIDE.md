# Running Basil with .NET Aspire - Complete Guide

## Why Use Aspire?

.NET Aspire transforms how you develop and run Basil by providing:

### 🎯 One Command to Rule Them All
```bash
cd aspire/Basil.AppHost
dotnet run
```

That's it! No more juggling terminals for backend and frontend.

### 📊 Beautiful Dashboard

Open http://localhost:15000 to see:

```
┌─────────────────────────────────────────────────────────┐
│  Basil Architecture Designer - Aspire Dashboard         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Services:                                              │
│  ✓ basil-backend    [Running]  http://localhost:8000  │
│  ✓ basil-frontend   [Running]  http://localhost:3000  │
│                                                         │
│  Logs:              Traces:            Metrics:        │
│  [Real-time view]   [Request flows]    [Charts]        │
│                                                         │
│  Health: All services healthy ✓                        │
└─────────────────────────────────────────────────────────┘
```

### 🔍 Observability Out of the Box

- **Logs**: See all service logs in one place, searchable and filterable
- **Traces**: Follow requests from frontend → backend → Python code
- **Metrics**: Request rates, response times, error rates
- **Health**: Auto-monitoring with alerts

## Installation

### Prerequisites

Install .NET 8.0 SDK:

**Windows:**
```powershell
winget install Microsoft.DotNet.SDK.8
```

**macOS:**
```bash
brew install dotnet@8
```

**Linux:**
```bash
wget https://dot.net/v1/dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --channel 8.0
```

### Install Aspire Workload

```bash
dotnet workload update
dotnet workload install aspire
```

### Verify Installation

```bash
dotnet --version  # Should be 8.0.x or later
```

## Running Basil with Aspire

### Method 1: Visual Studio 2022 (Windows)

1. Install Visual Studio 2022 v17.9 or later
2. Ensure ".NET Aspire" workload is installed
3. Open `aspire/Basil.sln`
4. Set `Basil.AppHost` as startup project
5. Press **F5**

Visual Studio will:
- ✅ Start Aspire Dashboard
- ✅ Install Python dependencies
- ✅ Install Node dependencies
- ✅ Start backend (FastAPI)
- ✅ Start frontend (React)
- ✅ Open browser to dashboard

### Method 2: Visual Studio Code (All Platforms)

1. Install C# extension
2. Open the `aspire` folder
3. Run:

```bash
cd Basil.AppHost
dotnet run
```

### Method 3: Command Line (All Platforms)

```bash
# Navigate to AppHost
cd aspire/Basil.AppHost

# Run with watch (hot reload)
dotnet watch run

# Or regular run
dotnet run
```

## First-Time Setup

When you first run, Aspire will:

1. **Restore .NET packages** (10-30 seconds)
2. **Install Python dependencies** from `backend/requirements.txt`
3. **Install Node packages** from `frontend/package.json`
4. **Start services** in order (backend first, then frontend)

**Total first-time setup: 2-5 minutes**

Subsequent runs are much faster (10-20 seconds).

## Using Aspire Dashboard

### 1. Access the Dashboard

After running, your browser opens to: **http://localhost:15000**

### 2. Navigate the Dashboard

#### **Resources Tab**

Shows all running services:

| Service | State | Endpoints |
|---------|-------|-----------|
| basil-backend | ✓ Running | http://localhost:8000 |
| basil-frontend | ✓ Running | http://localhost:3000 |

Click on a service to see:
- Environment variables
- Health status
- Restart option
- View logs

#### **Console Logs Tab**

Real-time logs from all services:

```
[basil-backend] INFO: Started server process
[basil-backend] INFO: Uvicorn running on http://0.0.0.0:8000
[basil-frontend] webpack compiled successfully
[basil-frontend] On Your Network: http://192.168.1.100:3000
```

**Features:**
- Filter by service
- Search logs
- Auto-scroll
- Copy logs

#### **Structured Logs Tab**

Queryable logs with filters:

```
Timestamp            | Level | Service        | Message
2024-01-15 10:30:42 | INFO  | basil-backend  | POST /api/design
2024-01-15 10:30:43 | INFO  | basil-backend  | Architecture generated
```

**Filters:**
- By timestamp range
- By log level (INFO, WARN, ERROR)
- By service
- By message content

#### **Traces Tab**

Distributed tracing across services:

```
Request: POST /api/design
├─ basil-frontend → basil-backend [120ms]
│  ├─ POST /api/design [115ms]
│  │  ├─ Problem analysis [45ms]
│  │  ├─ Agent grouping [30ms]
│  │  ├─ LLM selection [25ms]
│  │  └─ Architecture build [15ms]
│  └─ Response [5ms]
```

Click any trace to see:
- Timing breakdown
- Request/response data
- Errors (if any)

#### **Metrics Tab**

Performance metrics with charts:

**HTTP Requests:**
- Total requests
- Requests per second
- Response time (p50, p95, p99)

**Errors:**
- Error count
- Error rate
- Error types

**Custom Metrics:**
- Architectures designed
- Average agent count
- Cost estimates

### 3. Using the Application

From the dashboard:

1. Click **basil-frontend** endpoint → Opens http://localhost:3000
2. Use Basil normally
3. Watch logs and traces in real-time in the dashboard

### 4. Debugging

**View Errors:**
1. Go to **Structured Logs** tab
2. Filter: Level = ERROR
3. Click error to see full stack trace

**Trace Slow Requests:**
1. Go to **Traces** tab
2. Sort by duration
3. Click slowest trace
4. See timing breakdown

## Development Workflow

### Hot Reload

All services support hot reload:

**Backend (Python):**
- Edit `backend/api.py`
- Save → Auto-reloads
- See reload in dashboard logs

**Frontend (React):**
- Edit `frontend/src/App.js`
- Save → Hot reloads in browser
- See compilation in dashboard

**AppHost (C#):**
```bash
dotnet watch run
```
- Edit `Program.cs`
- Save → Restarts AppHost

### Debugging

**Python Backend:**
```bash
# In dashboard, note backend port
# Attach VS Code Python debugger to that port
```

**React Frontend:**
```bash
# Use browser DevTools
# Or attach VS Code JavaScript debugger
```

### Testing

Run tests while Aspire is running:

**Backend Tests:**
```bash
cd backend
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

Tests use the running services automatically!

## Configuration

### Environment Variables

Edit `aspire/Basil.AppHost/Program.cs`:

```csharp
var backend = builder.AddPythonProject("basil-backend", "../../backend", "api.py")
    .WithEnvironment("MY_VAR", "value")
    .WithEnvironment("API_KEY", builder.Configuration["ApiKey"]);
```

### Ports

Change ports in `Program.cs`:

```csharp
// Backend on port 8001 instead of 8000
.WithHttpEndpoint(port: 8001, name: "api")

// Frontend on port 3001 instead of 3000
.WithHttpEndpoint(port: 3001, name: "ui")
```

### Dashboard Port

Edit `aspire/Basil.AppHost/appsettings.json`:

```json
{
  "profiles": {
    "Basil.AppHost": {
      "applicationUrl": "http://localhost:16000"  // Changed from 15000
    }
  }
}
```

## Common Scenarios

### Scenario 1: Backend Only

Comment out frontend in `Program.cs`:

```csharp
// var frontend = builder.AddNpmApp(...);  // Commented out
```

Run just backend for API development.

### Scenario 2: Add Database

```csharp
var postgres = builder.AddPostgres("postgres")
    .WithPgAdmin()
    .AddDatabase("basildb");

var backend = builder.AddPythonProject("basil-backend", "../../backend", "api.py")
    .WithReference(postgres);
```

### Scenario 3: Add Redis Cache

```csharp
var redis = builder.AddRedis("cache");

var backend = builder.AddPythonProject("basil-backend", "../../backend", "api.py")
    .WithReference(redis);
```

## Production Deployment

### Deploy to Azure

```bash
# Install Azure Developer CLI
winget install microsoft.azd  # Windows
brew install azd              # macOS

# Initialize
cd aspire/Basil.AppHost
azd init

# Deploy
azd up
```

Aspire creates:
- ✅ Azure Container Apps
- ✅ Container Registry
- ✅ Application Insights
- ✅ Log Analytics
- ✅ All networking and security

### Generate Kubernetes Manifests

```bash
dotnet run --publisher manifest --output-path ./manifests
```

Deploy to any Kubernetes cluster:

```bash
kubectl apply -f manifests/
```

## Troubleshooting

### Problem: "Workload 'aspire' not found"

**Solution:**
```bash
dotnet workload install aspire
```

### Problem: Python dependencies not installing

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Problem: Node packages not installing

**Solution:**
```bash
cd frontend
npm install
```

### Problem: Ports already in use

**Solution:**
Change ports in `Program.cs` (see Configuration section)

### Problem: Dashboard not opening

**Solution:**
Manually open http://localhost:15000

### Problem: Services not starting

**Solution:**
1. Check dashboard console logs
2. Look for error messages
3. Verify Python and Node are in PATH

## Advantages Over Docker Compose

| Feature | Aspire | Docker Compose |
|---------|--------|----------------|
| Dashboard | ✅ Beautiful UI | ❌ CLI only |
| Real-time logs | ✅ Yes | ⚠️ Basic |
| Distributed tracing | ✅ Built-in | ❌ Requires Jaeger |
| Metrics | ✅ Built-in charts | ❌ Requires Prometheus |
| Hot reload | ✅ Native | ⚠️ Limited |
| IDE integration | ✅ VS 2022 | ❌ None |
| Cloud deployment | ✅ `azd up` | ❌ Manual |
| Service discovery | ✅ Automatic | ⚠️ Manual |
| Health monitoring | ✅ Automatic | ⚠️ Manual |

## Next Steps

1. **Run Aspire**: `cd aspire/Basil.AppHost && dotnet run`
2. **Open Dashboard**: http://localhost:15000
3. **Use Basil**: Click frontend link in dashboard
4. **Explore Logs**: Watch real-time logs
5. **View Traces**: See request flows
6. **Check Metrics**: Monitor performance

Happy developing with .NET Aspire! 🚀
