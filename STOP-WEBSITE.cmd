@echo off
cd /d "%~dp0"
set "PATH=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin;%ProgramFiles%\Docker\Docker\resources\bin;%PATH%"
docker compose stop
if errorlevel 1 pause
