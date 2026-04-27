var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => new { message = "Hello from CI/CD Deployed API!", timestamp = DateTime.UtcNow });

app.MapGet("/health", () => new { status = "healthy", runner = "wsl-self-hosted" });

app.MapGet("/deploy-info", () => new
{
    deployedAt = DateTime.UtcNow,
    environment = "WSL Self-Hosted Runner",
    framework = ".NET 8 ASP.NET Core"
});

app.MapGet("/whoami", () => new { 
    name = "Hermes Agent", 
    role = "CI/CD Assistant", 
    status = "Active",
    message = "Deployed successfully via GitHub Actions!"
});

app.Run();
