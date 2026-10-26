@echo off
cd /d "%~dp0"
set "PATH=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin;%ProgramFiles%\Docker\Docker\resources\bin;%PATH%"
docker info >nul 2>&1
if errorlevel 1 (
  echo Open Docker Desktop and wait until the engine is running, then try again.
  pause
  exit /b 1
)
docker compose up --build -d
if errorlevel 1 (
  pause
  exit /b 1
)
echo WebSite is starting at http://localhost:8001/
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" http://localhost:8001/
