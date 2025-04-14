"""Main entry point for the AdsGen API service.

This module initializes and configures the FastAPI application,
sets up logging, and manages project imports.
"""
import sys
from pathlib import Path
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.endpoints import default, users, test, auth, teams
from src.api.v1.endpoints import prompts
from src.utils.create_tables import create_tables


logging.getLogger('sqlalchemy.engine.Engine').disabled = True

# add project root directory to Python import path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for the application."""
    # Check and create tables on startup
    create_tables()
    yield
    # Cleanup on shutdown (if needed)

# build app for fast api
app = FastAPI(
    title="AdsGen API Service",
    description="This is an API service for advertising generation",
    version="0.1.0",
    lifespan=lifespan,
)

# configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins, production environment should restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routes
app.include_router(default, prefix="/api/default", tags=["Default"])
app.include_router(users, prefix="/api/users", tags=["Users"])
app.include_router(auth, prefix="/api/auth", tags=["Authentication"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["Prompts"])
app.include_router(teams, prefix="/api/teams", tags=["Teams"])
app.include_router(test, prefix="/api/test", tags=["Test"])
'''
# run app: integrate Ngrok and Uvicorn, one-click start
if __name__ == "__main__":
    from src.utils.ngrok_client import start_daemon, get_tunnel_url, stop_daemon
    from src.utils.create_tables import create_tables
    import uvicorn
    import atexit
    import signal
    import time

    # Check and create tables if needed
    create_tables()

    PORT = 8080

    def signal_handler():
        """Signal handler for the application."""
        print("closing ngrok tunnel...")
        stop_daemon()
        sys.exit(0)

    def exit_handler():
        """Exit handler for the application."""
        print("closing ngrok tunnel...")
        stop_daemon()

    # register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # register exit handler
    atexit.register(exit_handler)

    # start ngrok daemon
    if start_daemon(PORT):
        # get tunnel URL
        tunnel_url = get_tunnel_url()
        if tunnel_url:
            print(f"ngrok tunnel opened: {tunnel_url}")
        else:
            print("WARNING: unable to get ngrok tunnel URL")
    else:
        print("WARNING: unable to start ngrok daemon")
    try:
        # start Uvicorn server
        uvicorn.run("main_victor:app", host="0.0.0.0", port=PORT, reload=True)
    except KeyboardInterrupt:
        # ensure ngrok daemon is stopped when KeyboardInterrupt occurs
        print("closing ngrok tunnel...")
        stop_daemon()
    finally:
        # ensure ngrok daemon is stopped
        stop_daemon()
        # wait for a while to ensure all cleanup operations are completed
        time.sleep(0.5)
'''
