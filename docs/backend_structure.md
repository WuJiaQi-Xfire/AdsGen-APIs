# AdsGem Backend Structure

This document outlines the structure and organization of the AdsGem backend project, providing an overview of each component and its purpose.

## Project Structure

```
backend/
├── alembic/                  # Database migration tool
│   ├── env.py                # Alembic environment configuration
│   └── script.py.mako        # Template for migration scripts
├── container/                # Docker configuration
│   ├── docker-compose.yml    # Docker Compose configuration
│   └── Dockerfile            # Docker image definition
├── ngrok/                    # Ngrok tunnel configuration
│   ├── ngrok_config.json     # Ngrok configuration
│   └── ngrok_daemon.py       # Ngrok daemon process
├── requirements.txt          # Python dependencies
└── src/                      # Source code
    ├── api/                  # API routes and dependencies
    │   ├── deps.py           # API dependencies
    │   └── v1/               # API version 1
    │       └── endpoints/    # API endpoints
    │           ├── auth.py   # Authentication endpoints
    │           ├── default.py # Default endpoints
    │           ├── templates.py # Template endpoints
    │           ├── test.py   # Test endpoints
    │           └── users.py  # User management endpoints
    ├── celery/               # Celery task queue
    │   ├── tasks.py          # Task definitions
    │   └── worker.py         # Celery worker configuration
    ├── core/                 # Core functionality
    │   ├── celery_utils.py   # Celery utilities
    │   ├── config.py         # Application configuration
    │   ├── dependencies.py   # Core dependencies
    │   ├── init_db.py        # Database initialization
    │   └── security.py       # Security utilities
    ├── crud/                 # CRUD operations
    │   ├── base.py           # Base CRUD class
    │   ├── item.py           # Item CRUD operations
    │   └── user.py           # User CRUD operations
    ├── db/                   # Database configuration
    │   ├── base.py           # Base database models
    │   └── session.py        # Database session configuration
    ├── main.py               # Application entry point
    ├── models/               # Database models
    │   ├── generation.py     # Generation model
    │   ├── lora.py           # LoRA model
    │   ├── template.py       # Template model
    │   └── user.py           # User model
    ├── schemas/              # Pydantic schemas
    │   ├── generation.py     # Generation schemas
    │   ├── template.py       # Template schemas
    │   └── user.py           # User schemas
    ├── services/             # External services
    │   ├── comfy_service.py  # Comfyui service
    │   └── gpt_service.py    # GPT service
    │   └── file_service.py   # File service
    │   └── image_service.py  # Image processing service
    │   └── llm_service.py    # Language model service
    ├── tests/                # Tests
    │   ├── test_db.py        # Database tests
    │   └── test_user.py      # User tests
    └── utils/                # Utilities
    │   ├── file_utils.py     # File utilities
    |   ├── image_utils.py    # Image utilities
    |   ├── ngrok_client.py   # Ngrok client
    |   └── ngrok_manager.py  # Ngrok manager
    └── instructions/         # Master instructions
    │   ├── image_prompt.txt  # Instruction for templates with reference image
    │   └── text_prompt.txt   # Instruction for templates without reference image
    │   └── keyword_prompt.txt# Instruction to extract keywords based on input image
```

## Key Components

### API Layer (`src/api/`)

The API layer handles HTTP requests and responses, defining the endpoints that clients can interact with.

- **deps.py**: Defines API dependencies and a generic CRUD router for creating standard CRUD endpoints.
- **v1/endpoints/**: Contains API endpoint definitions for different resources.

### Database Layer (`src/db/`, `src/models/`, `src/crud/`)

The database layer manages data persistence and retrieval.

- **db/**: Contains database configuration and session management.
- **models/**: Defines SQLAlchemy ORM models representing database tables.
- **crud/**: Implements CRUD (Create, Read, Update, Delete) operations for each model.

### Schema Layer (`src/schemas/`)

The schema layer defines Pydantic models for request validation and response serialization.

- Each schema file corresponds to a specific resource (e.g., user, template, generation).
- Schemas define the structure of data for API requests and responses.

### Core Layer (`src/core/`)

The core layer contains essential functionality and configuration for the application.

- **config.py**: Application configuration settings.
- **security.py**: Security-related utilities (authentication, password hashing).
- **init_db.py**: Database initialization logic.

### Service Layer (`src/services/`)

The service layer integrates with external services and implements business logic.

- **image_service.py**: Handles image processing operations.
- **llm_service.py**: Integrates with language models for text generation.

### Utility Layer (`src/utils/`)

The utility layer provides helper functions and tools.

- **file_utils.py**: File handling utilities.
- **ngrok_client.py**: Client for interacting with Ngrok tunneling service.
- **ngrok_manager.py**: Management of Ngrok tunnels.

### Task Queue (`src/celery/`)

The task queue handles asynchronous and background processing.

- **tasks.py**: Defines Celery tasks.
- **worker.py**: Configures Celery worker.

### Testing (`src/tests/`)

The testing directory contains test cases for the application.

- **test_db.py**: Tests for database operations.
- **test_user.py**: Tests for user-related functionality.

## Application Flow

1. The application starts from `main.py`, which initializes the FastAPI application.
2. API routes are defined in the `api/v1/endpoints/` directory.
3. Requests are validated using Pydantic schemas from the `schemas/` directory.
4. Business logic is implemented in CRUD operations and services.
5. Data is persisted using SQLAlchemy ORM models.
6. Background tasks are handled by Celery.

## Key Features

- **User Management**: Registration, authentication, and user profile management.
- **Template Management**: Creation and management of templates.
- **Content Generation**: Generation of content using language models.
- **Ngrok Integration**: Exposing local services to the public internet for testing and development.
- **Async Database Operations**: Using SQLAlchemy's async capabilities for efficient database access.
- **Background Processing**: Using Celery for handling long-running tasks.

## Development Setup

The application can be run locally using Python or with Docker. It connects to a PostgreSQL database and can be exposed to the internet using Ngrok for testing and development purposes.
