# Advertising Generation Platform - Development TODO List

This list temptatively outlines the major development phases and tasks. Priorities and methods can be adjusted based on team decisions and MVP scope.

**Phase 1: Foundation & Core Backend Setup**

*   [x] **Setup Project Repositories:** Create Git repositories for frontend (React) and backend (Flask).
*   [ ] **Define Database Schema:** Use PostgreSQL. Define initial schemas for Users, Teams (basic structure), Templates (including sharing permissions), LORAs (including trigger words, clip skip, base strength), Generated Assets (including source template, prompt used).
*   [ ] **Implement Basic User Authentication:** Setup user registration, login, logout functionality (e.g., using Flask-Login, JWT). Include basic user profile management.
*   [x] **Setup Basic Flask Application:** Initialize Flask app, configure basic routes, database connection (e.g., using SQLAlchemy).
*   [ ] **Implement API Endpoints (Initial):** Create basic CRUD API endpoints for:
    *   User management (GET user info)
    *   Template management (Create, Read - List/Get, including permission checks)
    *   LORA management (Create/Upload with params, Read - List/Get, Delete)
*   [ ] **Setup Asynchronous Task Queue:** Integrate Celery with Redis or RabbitMQ for handling LLM calls and ComfyUI tasks.
*   [ ] **Initial Deployment Setup (Dev/Staging):** Configure basic deployment for the Flask app (e.g., using Docker + Gunicorn/Waitress) on a test Linux server. Define initial server specs (see recommendation below).

**Phase 2: Core Generation Logic - Text Input & Initial Image**

*   [ ] **Integrate Azure OpenAI API:** Create backend service/utility to interact with Azure OpenAI. Securely manage API keys.
*   [ ] **Implement Template Generation (Text Input - FR-02.1):**
    *   Create API endpoint to receive text description.
    *   Call Azure OpenAI service using the `system prompt for text description` logic.
    *   Parse LLM response and save the generated Advertising Prompt Template to the database (associating with user/team).
*   [ ] **Implement LORA/Art Style Management Backend:** Finalize DB schema and API endpoints for uploading (with params), storing, retrieving LORAs and Art Style keywords. Implement logic for applying default LORA params if not provided on upload.
*   [ ] **Integrate ComfyUI API (Workflow 1):**
    *   Create backend service/utility to interact with the ComfyUI API (Workflow 1 - initial 1024x1024 generation).
    *   Define the ComfyUI Workflow 1 JSON structure/API call.
*   [ ] **Implement Image Prompt Generation Logic (FR-04.3):**
    *   Create backend logic/service that takes Template structure, user keywords, art style, LORA info (including strength from UI), makes a separate LLM call to generate the final ComfyUI-ready image description string.
*   [ ] **Implement Image Generation Task (Workflow 1 - FR-04.4):**
    *   Create Celery task to:
        *   Receive Template ID, keywords, art style, LORA info (incl. strength).
        *   Execute Image Prompt Generation Logic (FR-04.3).
        *   Call the ComfyUI API service (Workflow 1) with the generated prompt.
        *   Handle ComfyUI response (success/failure), store generated image metadata (path/ID, prompt used, source template, user ID) in the database.
        *   Store the generated image file (e.g., cloud storage or mounted volume accessible by Flask).
        *   Update task status for frontend polling.

**Phase 3: Frontend Implementation - Core Workflow**

*   [ ] **Setup Basic React Application:** Initialize React app (e.g., using Create React App or Vite), setup routing (e.g., React Router).
*   [ ] **Implement Basic UI Layout:** Create main navigation, layout structure.
*   [ ] **Implement Authentication UI:** Login, Registration pages.
*   [ ] **Implement Template Creation UI (Text Input):** Form for text input, API call to backend (FR-02.1), display feedback.
*   [ ] **Implement Template Gallery UI:** Fetch and display user's templates and default templates (FR-03.3). Allow selection.
*   [ ] **Implement LORA/Art Style Gallery UI:** Fetch and display available LORAs (with associated params) and art styles. Implement LORA upload form (including fields for trigger words, clip skip, base strength). Implement LORA selection with strength slider (FR-06.1, FR-04.2).
*   [ ] **Implement Image Generation Form UI:** Select template, input keywords, select art style, select LORA (with strength slider) (FR-04.1, FR-04.2). Trigger generation API call (initiates Celery task).
*   [ ] **Implement Image Results Display UI:** Poll backend API for task status (Celery), display generated images (FR-04.5) when ready, show loading/progress indicators.

**Phase 4: Advanced Features & Refinements**

*   [ ] **Implement Template Generation (Layout/Intent Input - FR-02.2):** Backend API and Frontend UI.
*   [ ] **Implement Template Generation (Image Analysis Input - FR-02.3):**
    *   Backend API endpoint to receive image upload.
    *   Call LLM service using `system prompt for image description` logic with the uploaded image.
    *   Parse response and save template.
    *   Frontend UI for image upload.
*   [ ] **Implement Template Generation (PSD Upload - FR-02.4):**
    *   Backend API for PSD upload. Store PSD file. Optionally convert to PNG and trigger Image Analysis flow (FR-02.3) for template generation based on layout.
    *   Frontend UI for PSD upload.
*   [ ] **Implement Image Refinement (Aspect Ratio - FR-05.2):**
    *   Integrate ComfyUI API (Workflow 2 - 1:1, 9:16, 16:9 generation). Define Workflow 2 JSON/API call.
    *   Backend service/utility to call ComfyUI API (Workflow 2).
    *   Celery task for aspect ratio generation (takes source image ID, generates 3 variations).
    *   Frontend UI to select image and trigger aspect ratio generation task. Update results display.
*   [ ] **Implement Image Download Functionality (FR-05.3):**
    *   Backend API endpoints to serve image files (PNG, JPG) based on asset ID.
    *   Implement PSD compositing logic (using `psd-tools`/Pillow) triggered via a download request if an original PSD exists for the template.
    *   Backend API endpoint for PSD download.
    *   Frontend UI download buttons for available formats.
*   [ ] **Implement Template Editing/Refinement (FR-03.4):** Basic UI and backend logic to view/update template metadata (name, description). (Full prompt regeneration might be complex).
*   [ ] **Implement "Random Keyword" Exploration Feature (FR-04.6):** Backend logic to read keywords from CSV (initially). Frontend UI to trigger generation with random keywords from selected list. Allow user CSV upload.
*   [ ] **Refine Error Handling & User Feedback:** Implement comprehensive error handling for API calls (LLM, ComfyUI), task failures (Celery). Provide clear feedback to the user via UI notifications.
*   [ ] **Implement Caching:** Add Redis caching for LLM prompt generation results (if inputs are identical), potentially gallery listings.
*   [ ] **Implement Template Sharing Backend/UI (FR-06.3):** Add permission fields to Template model. Update API endpoints and UI to handle setting/checking permissions.

**Phase 5: Deployment & Operations**

*   [ ] **Finalize Production Deployment:** Configure production servers (App, DB, Queue, ComfyUI), networking, security groups.
*   [ ] **Setup Monitoring & Logging:** Integrate tools like Sentry, Grafana, Prometheus, or cloud provider equivalents.
*   [ ] **Implement CI/CD Pipeline:** Automate testing and deployment.
*   [ ] **Perform Load Testing:** Identify bottlenecks and scale resources accordingly.
*   [ ] **Setup Data Backups:** Configure regular database and file storage backups.
*   [ ] **Documentation:** Finalize user guides and technical documentation.

**Future Considerations / Post-MVP:**

*   [ ] Team/Organization Features (Sharing, Roles - FR-01, FR-03.5)
*   [ ] Advanced Template Editing/Versioning
*   [ ] A/B Testing Integration Hooks
*   [ ] Expansion to other industries (requires prompt engineering)
*   [ ] Admin Dashboard for managing users, default templates, LORAs.
