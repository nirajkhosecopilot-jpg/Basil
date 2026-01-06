using Aspire.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

// Add FastAPI Backend - Using startup script with virtual environment support
var backendScript = OperatingSystem.IsWindows() ? "start.bat" : "./start.sh";
var backend = builder.AddExecutable("basil-backend", backendScript, "../../backend")
    .WithHttpEndpoint(port: 8000, name: "api")
    .WithExternalHttpEndpoints();

// Add React Frontend - Using NPM (no Docker required)
var frontend = builder.AddNpmApp("basil-frontend", "../../frontend", "start")
    .WithHttpEndpoint(port: 3000, name: "ui")
    .WithEnvironment("BROWSER", "none")
    .WithExternalHttpEndpoints()
    .WaitFor(backend);

builder.Build().Run();
