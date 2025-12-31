using Aspire.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

// Add FastAPI Backend
var backend = builder.AddPythonProject("basil-backend", "../../backend", "api.py")
    .WithHttpEndpoint(port: 8000, name: "api")
    .WithEnvironment("PYTHONUNBUFFERED", "1")
    .WithEnvironment("HOST", "0.0.0.0")
    .WithEnvironment("PORT", "8000")
    .WithExternalHttpEndpoints();

// Add React Frontend (Node.js)
var frontend = builder.AddNpmApp("basil-frontend", "../../frontend", "start")
    .WithHttpEndpoint(port: 3000, name: "ui")
    .WithEnvironment("REACT_APP_API_URL", backend.GetEndpoint("api"))
    .WithEnvironment("BROWSER", "none") // Don't auto-open browser
    .WithExternalHttpEndpoints()
    .WaitFor(backend);

builder.Build().Run();
