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
echo 3. View logs
echo 4. Stop services
echo 5. Restart services
echo 6. Exit
echo.

set /p choice=Enter option (1-6): 

if "%choice%"=="1" goto deploy
if "%choice%"=="2" goto update
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto stop
if "%choice%"=="5" goto restart
if "%choice%"=="6" goto end

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

REM Rebuild and start containers
%COMPOSE_CMD% up -d --build

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

:end
echo.
echo Thank you for using AdsGem APIs Deployment Script!
echo.
exit /b 0
