using Aspire.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

// Add FastAPI Backend using Executable instead of PythonProject
var backend = builder.AddExecutable("basil-backend", "python", "../../backend", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload")
    .WithHttpEndpoint(port: 8000, name: "api")
    .WithEnvironment("PYTHONUNBUFFERED", "1")
    .WithExternalHttpEndpoints();

// Add React Frontend
var frontend = builder.AddNpmApp("basil-frontend", "../../frontend", "start")
    .WithHttpEndpoint(port: 3000, name: "ui")
    .WithEnvironment("BROWSER", "none") // Don't auto-open browser
    .WithExternalHttpEndpoints()
    .WaitFor(backend);

builder.Build().Run();
