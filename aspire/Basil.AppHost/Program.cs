using Aspire.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

// Add FastAPI Backend using Dockerfile (works with all Aspire versions)
var backend = builder.AddDockerfile("basil-backend", "../../", "Dockerfile.backend")
    .WithHttpEndpoint(port: 8000, targetPort: 8000, name: "api")
    .WithExternalHttpEndpoints();

// Add React Frontend using Dockerfile
var frontend = builder.AddDockerfile("basil-frontend", "../../frontend", "Dockerfile")
    .WithHttpEndpoint(port: 3000, targetPort: 3000, name: "ui")
    .WithEnvironment("REACT_APP_API_URL", "http://localhost:8000")
    .WithExternalHttpEndpoints()
    .WaitFor(backend);

builder.Build().Run();
