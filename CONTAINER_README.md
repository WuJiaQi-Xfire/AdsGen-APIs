# AdsGem APIs Containerization

This document provides instructions for containerizing and deploying the AdsGem APIs project using Docker.

## Project Structure

The containerization setup includes:

- Backend Dockerfile (`backend/container/Dockerfile`)
- Frontend Dockerfile (`frontend/container/Dockerfile`)
- Frontend Nginx configuration (`frontend/container/nginx.conf`)
- Docker Compose file (`docker-compose.yml`)
- Deployment scripts for Windows (`deploy.bat`) and Linux/macOS (`deploy.sh`)

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git (for updates)

## Deployment Instructions

### Using the Deployment Scripts

#### Windows

1. Run the deployment script:
   ```
   deploy.bat
   ```

2. Follow the on-screen menu to:
   - Deploy the application for the first time
   - Update the application
   - View logs
   - Stop or restart services

#### Linux/macOS

1. Make the script executable (if needed):
   ```
   chmod +x deploy.sh
   ```

2. Run the deployment script:
   ```
   ./deploy.sh
   ```

3. Follow the on-screen menu to manage the application.

### Manual Deployment

If you prefer not to use the deployment scripts, you can manually deploy using Docker Compose:

1. Build and start the containers:
   ```
   docker-compose up -d --build
   ```

2. To update the application:
   ```
   git pull
   docker-compose up -d --build
   ```

3. To stop the application:
   ```
   docker-compose down
   ```

## Accessing the Application

- Frontend: http://localhost
- Backend API: http://localhost/api

## Environment Variables

The application uses environment variables for configuration. These are set in the `.env` file and passed to the containers through the Docker Compose file.

Key environment variables include:
- Database connection details
- API keys for external services
- Configuration settings

## Data Persistence

PostgreSQL data is persisted using a Docker volume (`postgres_data`). This ensures that your database data is preserved even if the containers are removed.

## Troubleshooting

If you encounter issues:

1. Check the logs:
   ```
   docker-compose logs
   ```

2. Ensure all required environment variables are set.

3. Verify that ports 80 and 8000 are not already in use on your host machine.

4. If the database connection fails, ensure the PostgreSQL container is running:
   ```
   docker-compose ps
   ```

## One-Click Update Process

The deployment scripts provide a one-click update process that:

1. Pulls the latest code from the Git repository
2. Rebuilds the Docker images with the updated code
3. Restarts the containers with minimal downtime

This ensures that your application is always running the latest version of the code.
