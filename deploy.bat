@echo off
echo ===== AdsGem APIs Deployment Script =====
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Docker is not installed or not in PATH. Please install Docker and try again.
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Warning: docker-compose command not found, trying docker compose...
    set COMPOSE_CMD=docker compose
) else (
    set COMPOSE_CMD=docker-compose
)

:menu
echo Please select an operation:
echo 1. First-time deployment
echo 2. Update application
echo 3. Start with existing images (no rebuild)
echo 4. View logs
echo 5. Stop services
echo 6. Restart services
echo 7. Exit
echo.

set /p choice=Enter option (1-7): 

if "%choice%"=="1" goto deploy
if "%choice%"=="2" goto update
if "%choice%"=="3" goto start_existing
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto stop
if "%choice%"=="6" goto restart
if "%choice%"=="7" goto end

echo Invalid option, please try again.
goto menu

:deploy
echo.
echo === Starting first-time deployment ===
echo.

REM Build and start containers
%COMPOSE_CMD% up -d --build

echo.
echo Deployment complete! Application is running.
echo Frontend URL: http://localhost
echo Backend API URL: http://localhost/api
echo.
goto menu

:update
echo.
echo === Starting application update ===
echo.

REM Pull latest code
git pull

REM Stop running containers first
echo Stopping running containers...
%COMPOSE_CMD% down

REM Rebuild and start containers
echo Rebuilding and starting containers...
%COMPOSE_CMD% up -d --build

REM Remove dangling images (None:None)
echo Removing dangling images...
docker image prune -f

echo.
echo Update complete! Application has been restarted.
echo.
goto menu

:logs
echo.
echo === View Logs ===
echo.
echo 1. View all services logs
echo 2. View backend logs
echo 3. View frontend logs
echo 4. View database logs
echo 5. Return to main menu
echo.

set /p log_choice=Select option (1-5): 

if "%log_choice%"=="1" (
    %COMPOSE_CMD% logs --tail=100 -f
    goto logs
)
if "%log_choice%"=="2" (
    %COMPOSE_CMD% logs --tail=100 -f backend
    goto logs
)
if "%log_choice%"=="3" (
    %COMPOSE_CMD% logs --tail=100 -f frontend
    goto logs
)
if "%log_choice%"=="4" (
    %COMPOSE_CMD% logs --tail=100 -f postgres
    goto logs
)
if "%log_choice%"=="5" goto menu

echo Invalid option, please try again.
goto logs

:stop
echo.
echo === Stopping services ===
echo.
%COMPOSE_CMD% down
echo All services have been stopped.
echo.
goto menu

:restart
echo.
echo === Restarting services ===
echo.
%COMPOSE_CMD% restart
echo All services have been restarted.
echo.
goto menu

:start_existing
echo.
echo === Starting with existing images (no rebuild) ===
echo.

REM Stop running containers first
echo Stopping running containers...
%COMPOSE_CMD% down

REM Start containers without rebuilding
echo Starting containers with existing images...
%COMPOSE_CMD% up -d

echo.
echo Start complete! Application is running with existing images.
echo Frontend URL: http://localhost
echo Backend API URL: http://localhost/api
echo.
goto menu

:end
echo.
echo Thank you for using AdsGem APIs Deployment Script!