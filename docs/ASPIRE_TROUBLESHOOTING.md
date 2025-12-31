# Aspire Troubleshooting Guide

## Common Issues and Solutions

### 1. "The executable python could not be found in the virtual environment"

**Problem:** Aspire expects Python in a virtual environment but can't find it.

**Solution:** Use `AddExecutable` instead of `AddPythonProject` to use system Python.

**Already Fixed** in the latest version! The `Program.cs` now uses:

```csharp
var backend = builder.AddExecutable("basil-backend", "python", "../../backend",
    "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload")
```

### 2. Missing Python Dependencies

**Problem:** Backend fails to start due to missing packages.

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### 3. Missing Node Dependencies

**Problem:** Frontend fails to start.

**Solution:**
```bash
cd frontend
npm install
```

### 4. Port Already in Use

**Problem:** Ports 3000, 8000, or 15000 already in use.

**Solution:** Change ports in `aspire/Basil.AppHost/Program.cs`:
```csharp
.WithHttpEndpoint(port: 8001, name: "api")  // Change backend port
.WithHttpEndpoint(port: 3001, name: "ui")   // Change frontend port
```

### 5. Python Not Found

**Problem:** Aspire can't find `python` command.

**Solutions:**

**Windows:**
- Ensure Python is in PATH
- Try `python3` instead of `python`:
  ```csharp
  builder.AddExecutable("basil-backend", "python3", ...)
  ```

**macOS/Linux:**
- Use `python3`:
  ```csharp
  builder.AddExecutable("basil-backend", "python3", ...)
  ```
- Or create alias: `alias python=python3`

### 6. Node/NPM Not Found

**Problem:** Aspire can't find npm.

**Solution:**
- Install Node.js: https://nodejs.org
- Verify: `npm --version`

### 7. Dashboard Not Opening

**Problem:** Dashboard doesn't auto-open.

**Solution:** Manually navigate to http://localhost:15000

### 8. Services Show "Exited" Status

**Problem:** Services start but immediately exit.

**Debug Steps:**
1. Open Aspire dashboard
2. Click on failed service
3. View "Console Logs" tab
4. Check error messages

Common causes:
- Missing dependencies
- Port conflicts
- Invalid paths in `Program.cs`

### 9. CORS Errors in Frontend

**Problem:** Frontend can't connect to backend.

**Solution:** Backend CORS is already configured for development. If issues persist:

```python
# In backend/api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 10. .NET SDK Not Found

**Problem:** `dotnet: command not found`

**Solution:**

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

### 11. Aspire Workload Not Installed

**Problem:** `The workload 'aspire' could not be found`

**Solution:**
```bash
dotnet workload update
dotnet workload install aspire
```

## Quick Verification

Run these commands to verify your setup:

```bash
# Check .NET
dotnet --version  # Should be 8.0.x or later

# Check Python
python --version  # or python3 --version

# Check Node
node --version
npm --version

# Check Aspire workload
dotnet workload list  # Should show 'aspire'
```

## Still Having Issues?

1. **Check Console Logs** in Aspire dashboard
2. **Verify paths** in `Program.cs` are correct relative to AppHost
3. **Ensure dependencies** are installed (Python packages, npm packages)
4. **Try manual start** to isolate the issue:
   ```bash
   # Start backend manually
   cd backend && python -m uvicorn api:app --reload

   # Start frontend manually
   cd frontend && npm start
   ```

## Alternative: Run Without Aspire

If Aspire continues to have issues, you can still run manually:

**Terminal 1 (Backend):**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install
npm start
```

Or use **Docker Compose**:
```bash
docker-compose up
```
