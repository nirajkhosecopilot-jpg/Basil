using Aspire.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

// Add FastAPI Backend - Using executable (no Docker required)
var pythonPath = OperatingSystem.IsWindows() ? "python" : "python3";
var backend = builder.AddExecutable("basil-backend", pythonPath, "../../backend",
        "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload")
    .WithHttpEndpoint(port: 8000, name: "api")
    .WithExternalHttpEndpoints();

// Add React Frontend - Using NPM (no Docker required)
var frontend = builder.AddNpmApp("basil-frontend", "../../frontend", "start")
    .WithHttpEndpoint(port: 3000, name: "ui")
    .WithEnvironment("BROWSER", "none")
    .WithExternalHttpEndpoints()
    .WaitFor(backend);

builder.Build().Run();
