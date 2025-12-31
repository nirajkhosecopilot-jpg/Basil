# Basil - .NET Aspire Integration

This directory contains the .NET Aspire solution for hosting Basil's React frontend and FastAPI backend.

## What is .NET Aspire?

.NET Aspire is an opinionated, cloud-ready stack for building observable, production-ready distributed applications. It provides:

- 🚀 **Orchestration**: Run multiple services together seamlessly
- 📊 **Dashboard**: Beautiful UI for monitoring services
- 🔍 **Observability**: Built-in OpenTelemetry for logs, metrics, and traces
- 🏥 **Health Checks**: Automatic service health monitoring
- 🔗 **Service Discovery**: Easy inter-service communication
- 🛡️ **Resilience**: Built-in retry policies and circuit breakers

## Architecture

```
┌─────────────────────────────────────────┐
│      .NET Aspire Dashboard              │
│      http://localhost:15000             │
│   ┌─────────────────────────────────┐   │
│   │  Service Logs & Metrics         │   │
│   │  OpenTelemetry Traces           │   │
│   │  Health Status                  │   │
│   └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ Manages
               ▼
    ┌──────────────────────┐
    │   Basil.AppHost      │
    │   (Orchestrator)     │
    └──────┬───────────┬───┘
           │           │
           ▼           ▼
    ┌──────────┐  ┌──────────┐
    │ Backend  │  │ Frontend │
    │ :8000    │  │ :3000    │
    │ FastAPI  │  │ React    │
    └──────────┘  └──────────┘
```

## Prerequisites

- .NET 8.0 SDK or later
- Python 3.9+
- Node.js 18+
- Docker Desktop (optional, for container deployments)

## Quick Start

### Option 1: Using Visual Studio 2022

1. Open `aspire/Basil.sln` in Visual Studio 2022 (v17.8 or later)
2. Set `Basil.AppHost` as the startup project
3. Press F5 to run

### Option 2: Using .NET CLI

```bash
cd aspire/Basil.AppHost
dotnet run
```

### Option 3: Using Visual Studio Code

```bash
cd aspire/Basil.AppHost
dotnet watch run
```

## What Happens When You Run

1. **Aspire Dashboard** opens at http://localhost:15000
2. **Backend (FastAPI)** starts on http://localhost:8000
3. **Frontend (React)** starts on http://localhost:3000
4. **Services are monitored** with health checks every 30 seconds
5. **Logs, metrics, and traces** are collected automatically

## Accessing the Application

| Service | URL | Description |
|---------|-----|-------------|
| **Aspire Dashboard** | http://localhost:15000 | Monitoring and telemetry |
| **Basil Frontend** | http://localhost:3000 | React UI |
| **Basil Backend** | http://localhost:8000 | FastAPI REST API |
| **API Docs** | http://localhost:8000/docs | Swagger/OpenAPI docs |

## Project Structure

```
aspire/
├── Basil.sln                    # Visual Studio solution
├── Basil.AppHost/               # Aspire orchestrator
│   ├── Program.cs               # Service configuration
│   ├── appsettings.json
│   └── Properties/
│       └── launchSettings.json
└── Basil.ServiceDefaults/       # Shared service configuration
    └── Extensions.cs            # Telemetry & health checks
```

## How It Works

### Basil.AppHost/Program.cs

This is the orchestrator that configures and runs all services:

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Add FastAPI Backend
var backend = builder.AddPythonProject("basil-backend", "../../backend", "api.py")
    .WithHttpEndpoint(port: 8000, name: "api")
    .WithExternalHttpEndpoints();

// Add React Frontend
var frontend = builder.AddNpmApp("basil-frontend", "../../frontend", "start")
    .WithHttpEndpoint(port: 3000, name: "ui")
    .WithEnvironment("REACT_APP_API_URL", backend.GetEndpoint("api"))
    .WaitFor(backend);  // Frontend waits for backend to be ready

builder.Build().Run();
```

### Key Features

**1. Service Discovery**
```csharp
.WithEnvironment("REACT_APP_API_URL", backend.GetEndpoint("api"))
```
Frontend automatically gets the backend URL - no hardcoding!

**2. Dependency Management**
```csharp
.WaitFor(backend)
```
Frontend waits for backend to be healthy before starting.

**3. Health Checks**
Aspire automatically monitors:
- `/health` endpoint on backend
- Process health for frontend
- Custom health checks from ServiceDefaults

**4. Telemetry**
Automatically collects:
- HTTP request/response logs
- Performance metrics
- Distributed traces
- Error tracking

## Aspire Dashboard Features

The dashboard (http://localhost:15000) provides:

### Resources View
- See all running services
- Check status (Running, Starting, Stopped)
- View endpoints and ports
- Monitor resource usage

### Console Logs
- Real-time logs from all services
- Filter by service
- Search logs
- Color-coded by severity

### Structured Logs
- Queryable structured logging
- Filter by level, service, time
- View request traces

### Traces
- Distributed tracing with OpenTelemetry
- See request flows across services
- Identify performance bottlenecks
- Trace errors end-to-end

### Metrics
- Request counts and rates
- Response times (p50, p95, p99)
- Error rates
- Custom metrics

## Configuration

### Environment Variables

Set in `Basil.AppHost/Program.cs`:

```csharp
// Backend
.WithEnvironment("PYTHONUNBUFFERED", "1")
.WithEnvironment("HOST", "0.0.0.0")
.WithEnvironment("PORT", "8000")

// Frontend
.WithEnvironment("REACT_APP_API_URL", backend.GetEndpoint("api"))
.WithEnvironment("BROWSER", "none")
```

### Ports

Configure in `appsettings.json`:

```json
{
  "profiles": {
    "Basil.AppHost": {
      "applicationUrl": "http://localhost:15000"
    }
  }
}
```

## Development Workflow

### Hot Reload

Both services support hot reload:

- **Backend**: FastAPI auto-reloads on code changes
- **Frontend**: React hot-reloads automatically
- **AppHost**: Use `dotnet watch run` for hot reload

### Debugging

**Visual Studio:**
1. Set breakpoints in Python or JavaScript
2. Attach debugger to running process
3. Debug through Aspire dashboard

**VS Code:**
1. Use Python or JavaScript debugger
2. Attach to process
3. View in Aspire dashboard

## Production Deployment

### Azure Container Apps

Aspire can deploy directly to Azure:

```bash
cd aspire/Basil.AppHost
azd init
azd up
```

This creates:
- Container Apps for frontend and backend
- Container Registry
- Log Analytics workspace
- Application Insights
- Managed identities

### Kubernetes

Generate Kubernetes manifests:

```bash
dotnet run --publisher manifest
```

This creates `manifest.json` which can be deployed to any Kubernetes cluster.

### Docker Compose

Generate Docker Compose file:

```bash
dotnet run --publisher docker-compose
```

## Advantages of Aspire for Basil

### ✅ Unified Development Experience
- Run all services with one command
- Single dashboard for all logs and metrics
- Consistent configuration

### ✅ Better Observability
- See request flows across services
- Identify performance issues quickly
- Trace errors end-to-end

### ✅ Production-Ready
- Built-in health checks
- Automatic retries and circuit breakers
- Easy deployment to cloud

### ✅ Service Discovery
- No hardcoded URLs
- Automatic endpoint configuration
- Environment-based configuration

### ✅ Developer Productivity
- Hot reload for all services
- Clear error messages
- Beautiful monitoring UI

## Troubleshooting

### Services Not Starting

Check Aspire dashboard for errors:
1. Open http://localhost:15000
2. Click on failing service
3. View console logs

### Port Conflicts

Change ports in `Program.cs`:

```csharp
.WithHttpEndpoint(port: 8001, name: "api")  // Changed from 8000
```

### Python Dependencies

Ensure Python environment is set up:

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-aspire.txt
```

### Node Dependencies

Ensure Node packages are installed:

```bash
cd frontend
npm install
```

## Comparison: Aspire vs Docker Compose

| Feature | .NET Aspire | Docker Compose |
|---------|-------------|----------------|
| **Dashboard** | ✅ Beautiful built-in UI | ❌ CLI only |
| **Logs** | ✅ Real-time, searchable | ⚠️ Basic |
| **Metrics** | ✅ Built-in | ❌ Need Prometheus |
| **Traces** | ✅ OpenTelemetry | ❌ Need Jaeger |
| **Hot Reload** | ✅ Supported | ⚠️ Limited |
| **Service Discovery** | ✅ Automatic | ⚠️ Manual |
| **Health Checks** | ✅ Built-in | ⚠️ Manual |
| **Cloud Deploy** | ✅ `azd up` | ❌ Manual |
| **IDE Integration** | ✅ VS 2022 | ⚠️ Limited |

## Additional Resources

- [.NET Aspire Documentation](https://learn.microsoft.com/dotnet/aspire)
- [Aspire GitHub Repository](https://github.com/dotnet/aspire)
- [Aspire Samples](https://github.com/dotnet/aspire-samples)

## Next Steps

1. **Run the application**: `cd aspire/Basil.AppHost && dotnet run`
2. **Explore the dashboard**: http://localhost:15000
3. **Use Basil**: http://localhost:3000
4. **View API docs**: http://localhost:8000/docs
5. **Check logs and traces** in the Aspire dashboard

Happy architecting with .NET Aspire! 🚀
