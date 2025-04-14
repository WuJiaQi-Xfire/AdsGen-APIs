# Route module initialization file
# This file allows Python to treat the directory as a package
# and allows importing modules from app.routers

# Import router objects from each route module
from src.api.v1.endpoints.default import router as default
from src.api.v1.endpoints.users import router as users
from src.api.v1.endpoints.test import router as test
from src.api.v1.endpoints.auth import router as auth
from src.api.v1.endpoints.teams import router as teams
