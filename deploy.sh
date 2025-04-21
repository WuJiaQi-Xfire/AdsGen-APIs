#!/bin/bash

echo "===== AdsGem APIs Deployment Script ====="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "Warning: docker-compose command not found, using docker compose..."
    COMPOSE_CMD="docker compose"
else
    echo "Error: Neither docker-compose nor docker compose is available. Please install Docker Compose and try again."
    exit 1
fi

# Make script executable
chmod +x "$0"

# Main menu function
show_menu() {
    echo "Please select an operation:"
    echo "1. First-time deployment"
    echo "2. Update application"
    echo "3. View logs"
    echo "4. Stop services"
    echo "5. Restart services"
    echo "6. Exit"
    echo
    read -p "Enter option (1-6): " choice
    
    case $choice in
        1) deploy ;;
        2) update ;;
        3) view_logs ;;
        4) stop_services ;;
        5) restart_services ;;
        6) exit_script ;;
        *) echo "Invalid option, please try again."; show_menu ;;
    esac
}

# Deploy function
deploy() {
    echo
    echo "=== Starting first-time deployment ==="
    echo
    
    # Build and start containers
    $COMPOSE_CMD up -d --build
    
    echo
    echo "Deployment complete! Application is running."
    echo "Frontend URL: http://localhost"
    echo "Backend API URL: http://localhost/api"
    echo
    show_menu
}

# Update function
update() {
    echo
    echo "=== Starting application update ==="
    echo
    
    # Pull latest code
    git pull
    
    # Rebuild and start containers
    $COMPOSE_CMD up -d --build
    
    echo
    echo "Update complete! Application has been restarted."
    echo
    show_menu
}

# View logs function
view_logs() {
    echo
    echo "=== View Logs ==="
    echo
    echo "1. View all services logs"
    echo "2. View backend logs"
    echo "3. View frontend logs"
    echo "4. View database logs"
    echo "5. Return to main menu"
    echo
    
    read -p "Select option (1-5): " log_choice
    
    case $log_choice in
        1) $COMPOSE_CMD logs --tail=100 -f; view_logs ;;
        2) $COMPOSE_CMD logs --tail=100 -f backend; view_logs ;;
        3) $COMPOSE_CMD logs --tail=100 -f frontend; view_logs ;;
        4) $COMPOSE_CMD logs --tail=100 -f postgres; view_logs ;;
        5) show_menu ;;
        *) echo "Invalid option, please try again."; view_logs ;;
    esac
}

# Stop services function
stop_services() {
    echo
    echo "=== Stopping services ==="
    echo
    $COMPOSE_CMD down
    echo "All services have been stopped."
    echo
    show_menu
}

# Restart services function
restart_services() {
    echo
    echo "=== Restarting services ==="
    echo
    $COMPOSE_CMD restart
    echo "All services have been restarted."
    echo
    show_menu
}

# Exit function
exit_script() {
    echo
    echo "Thank you for using AdsGem APIs Deployment Script!"
    echo
    exit 0
}

# Start the script
show_menu
