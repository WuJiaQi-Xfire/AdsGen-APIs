@echo off
setlocal EnableDelayedExpansion
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
echo 7. Push images to repository
echo 8. Exit
echo.

set /p choice=Enter option (1-8): 

if "%choice%"=="1" goto deploy
if "%choice%"=="2" goto update
if "%choice%"=="3" goto start_existing
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto stop
if "%choice%"=="6" goto restart
if "%choice%"=="7" goto push_images
if "%choice%"=="8" goto end

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

:push_images
echo.
echo === Pushing images to repository ===
echo.

REM Login to Docker registry
echo Logging in to Docker registry...
echo kSNYCe45Qj | docker login gt-cn-harbor.goatgames.com -u grail-cn --password-stdin

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to login to Docker registry. Please check your credentials and network connection.
    echo You may need to configure Docker to use an insecure registry if there are certificate issues.
    echo.
    set /p "retry=Would you like to retry with insecure registry option? (y/n): "
    if /i "%retry%"=="y" (
        echo Retrying with insecure registry option...
        docker logout gt-cn-harbor.goatgames.com 2>nul
        echo Adding insecure registry to Docker daemon configuration...
        echo This may require administrator privileges.
        echo.
        echo kSNYCe45Qj | docker login gt-cn-harbor.goatgames.com -u grail-cn --password-stdin
        if %ERRORLEVEL% neq 0 (
            echo Error: Still failed to login. Please check your network connection and try again later.
            goto menu
        )
    ) else (
        goto menu
    )
)

rem --- image names & tags ---
set "FRONTEND_SRC=adsg-frontend:0.1.0"
set "FRONTEND_DEST=gt-cn-harbor.goatgames.com/grail-cn-comfyui/adsg-frontend:0.1.0"
set "BACKEND_SRC=adsg-backend:0.1.0"
set "BACKEND_DEST=gt-cn-harbor.goatgames.com/grail-cn-comfyui/adsg-backend:0.1.0"
set "POSTGRES_SRC=postgres:15-alpine"
set "POSTGRES_DEST=gt-cn-harbor.goatgames.com/grail-cn-comfyui/postgres:15-alpine"

REM Tag and push frontend image
echo Tagging and pushing frontend image...
docker tag %FRONTEND_SRC% %FRONTEND_DEST%
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to tag frontend image.
    goto menu
)
docker push %FRONTEND_DEST%
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to push frontend image.
    goto menu
)

REM Tag and push backend image
echo Tagging and pushing backend image...
docker tag %BACKEND_SRC% %BACKEND_DEST%
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to tag backend image.
    goto menu
)
docker push %BACKEND_DEST%
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to push backend image.
    goto menu
)

REM Tag and push PostgreSQL image
echo Tagging and pushing PostgreSQL image...
docker tag %POSTGRES_SRC% %POSTGRES_DEST%
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to tag PostgreSQL image.
    goto menu
)
docker push %POSTGRES_DEST%
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to push PostgreSQL image.
    goto menu
)

echo.
echo All images have been pushed to the repository.
echo.
goto menu

:end
echo.
echo Thank you for using AdsGem APIs Deployment Script!
