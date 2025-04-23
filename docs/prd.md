# Project Requirements Document: Advertising Generation Platform

**Version:** 1.0
**Date:** 2025-04-03

## 1. Introduction

The Advertising Generation Platform is a web-based Marketing Assistance Tool designed to empower marketing teams, initially within the gaming industry, to efficiently create high-quality, market-ready advertising images and concepts. It leverages AI (LLMs and Image Generation models) to translate user ideas into visual advertising materials with minimal friction, supporting various input methods and customization options.

## 2. Goals

*   **Streamline Ad Creation:** Drastically reduce the time and manual effort involved in generating advertising concepts and final image assets.
*   **Enhance Quality & Relevance:** Produce high-quality, contextually relevant advertising images suitable for market use.
*   **Empower Users:** Provide flexible input methods (text, layout, image analysis, PSD) to cater to different creative workflows.
*   **Facilitate Customization:** Allow users to integrate specific art styles (keywords, LORAs) into the generation process.
*   **Promote Collaboration:** Enable sharing of templates and assets within teams (future goal).
*   **Build a Scalable Foundation:** Create a platform architecture that can support user growth and potential expansion into other market verticals.

## 3. Target Audience

*   **Primary:** Marketing professionals, graphic designers, and content creators in the gaming industry.
*   **Secondary (Potential Future):** Marketing teams in other industries requiring rapid visual content generation.

## 4. User Cases

*   **As a Marketing Manager, I want to quickly generate multiple ad concepts based on a simple text description so that I can explore different visual directions efficiently.**
*   **As a Graphic Designer, I want to upload a competitor's ad image to analyze its layout and intent so that I can create a similar structured ad for my own campaign.**
*   **As a Content Creator, I want to define a specific ad layout (e.g., split-screen progression) and intent so that the generated images consistently follow my desired structure.**
*   **As a Marketing Artist, I want to upload and use specific LORA models so that the generated images match my game's unique art style.**
*   **As a User, I want to upload a PSD template so that the generated images can be easily integrated or composited with my existing UI elements and branding.**
*   **As a User, I want to generate variations of a successful ad image in different aspect ratios (1:1, 9:16, 16:9) so that I can deploy the ad across multiple platforms.**
*   **As a User, I want to browse a gallery of pre-defined and my own saved advertising templates so that I can reuse successful structures.**
*   **As a User, I want to download the final images in both standard formats (PNG, JPG) and PSD format for further editing.**

## 5. Functional Requirements

### FR-01: User Account Management
*   Users must be able to register, log in, and log out.
*   (Future) User roles and permissions (e.g., admin, user, team member).
*   (Future) Team/Organization management.

### FR-02: Input Methods for Template Creation
*   **FR-02.1: Text Input:** Allow users to input a natural language description of the desired ad concept. The system shall use an LLM (Azure OpenAI) with the text system prompt to generate an Advertising Prompt Template.
*   **FR-02.2: Layout & Intent Input:** Allow users to specify layout structure (e.g., "50/50 vertical split") and intent (e.g., "poor vs rich comparison"). The system shall use an LLM (Azure OpenAI) with the text system prompt to generate an Advertising Prompt Template.
*   **FR-02.3: Image Analysis Input:** Allow users to upload an image. The system shall use an LLM (Azure OpenAI) guided by the `system prompt for images` logic to analyze the image and generate an Advertising Prompt Template based on the inferred layout and intent.
*   **FR-02.4: PSD Upload:** Allow users to upload an image or potentially a PSD file containing the layout structure the users want to receive as output. The system may convert the PSD to a PNG for layout analysis (similar to FR-02.3) using the `system prompt for images`. -If uploaded- The PSD file will be stored and used for final image compositing (FR-05.3).

### FR-03: Advertising Prompt Template Management
*   **FR-03.1: Generation:** The system must generate reusable Advertising Prompt Templates based on user inputs (FR-02). Templates define structure, intent, and placeholders.
*   **FR-03.2: Storage:** Templates must be saved and associated with the user/team account.
*   **FR-03.3: Gallery:** Provide a gallery view for users to browse, select, and manage their saved templates and default templates provided by teh system itself.
*   **FR-03.4: Editing:** Allow users to view and potentially refine saved templates (details TBD).
*   **FR-03.5: Sharing:** (Future) Allow sharing of templates within teams or publicly.

### FR-04: Image Generation Workflow
*   **FR-04.1: Template Selection:** Users must select an Advertising Prompt Template from the gallery or their own generated Advertising Prompt Templates.
*   **FR-04.2: Parameter Input:** Users must provide specific parameters for generation:
    *   Keywords/Theme (text input) or randomized set of keywords.
    *   Art Style (selection from predefined list or text input).
    *   LORA selection (from user's or default gallery). Users can adjust LORA strength via a slider (default/user-defined base strength applied). Default parameters (trigger words, clip skip) are associated with uploaded LORAs.
*   **FR-04.3: Image Prompt Generation:** The system must use a separate LLM call to combine the selected Advertising template structure/rules with the user-provided parameters (Keywords, Art Style) to generate a final, detailed image prompt suitable for ComfyUI.
*   **FR-04.4: Initial Image Generation (ComfyUI Workflow 1):** Send the generated prompt to ComfyUI to generate concept images.
    *   ***Parameters:** Default parameters (Clip skip, trigger words) + Strength + Image prompt*
        *   Generate 1 image when testing a new template.
        *   Generate a configurable number of images (TBD based on cost/performance) for bulk generation runs.
        *   Base resolution: 1024x1024.
*   **FR-04.5: Image Review:** Display the generated image(s) to the user.
*   **FR-04.6: Iteration:** Allow users to trigger new generations using the same template with different keywords. Support for "random keywords" sourced initially from provided CSV files, later potentially from user-uploaded lists.

### FR-05: Image Refinement & Output
*   **FR-05.1: Image Selection:** Users must be able to select one or more promising images from the initial generation.
*   **FR-05.2: Aspect Ratio Generation (ComfyUI Workflow 2):** For selected images, allow users to request generation of variations in standard aspect ratios: 1:1, 9:16, and 16:9. Existing ComfyUI workflows handle resizing/outpainting.
*   **FR-05.3: Download Options:** Allow users to download selected final images (and their aspect ratio variations) as:
    *   PNG files.
    *   JPG files.
    *   PSD files: If an original PSD was uploaded for the template, the generated image variation will be composited into the PSD (using `psd-tools`/Pillow) by inserting it as a layer above the background but below other existing layers.
    **Note:** If users require additional aspect ratios, they must provide the psd files for those aspect ratio.
    **PSD Files Requirements:** Background layer must be always present 
        * 1:1 Resolution: 1080x1080 px
        * 16:9 Resolution: 1080x1920 px
        * 9:16 Resolution: 1920x1080 px

### FR-06: Asset Galleries
*   **FR-06.1: LORA Gallery:** Allow users to upload, view, and manage their LORA models (defining default trigger words, clip skip, base strength). Provide default LORAs. Storage limits TBD with Ops team (typical size < 300MB). Interface to include strength slider during selection (FR-04.2).
*   **FR-06.2: Art Style Management:** Maintain a list of suggested art style keywords. Allow users to input custom keywords if they need.
*   **FR-06.3: Template Gallery Sharing:** Implement user-defined sharing permissions for templates (Public, Team-based, Private). (Requires User/Team structure from FR-01).

## 6. Non-Functional Requirements

*   **NFR-01: Performance:**
    *   API response times for LLM calls should be reasonable (target < 10 seconds).
    *   Image generation times will depend on ComfyUI but should be managed via asynchronous processing (queuing) (TBD according to Ops solution deployment provided). Users should receive feedback on job status.
    *   Web application UI should be responsive (< 2 seconds load time for key pages).
*   **NFR-02: Scalability:** 
    *   The application server must handle an initial estimate of (**X**) oncurrent users (**X** = TBD).
    *   ComfyUI infrastructure must be scalable (potentially horizontally) to handle varying image generation loads. (TBD)
    *   Database must handle growing data (users, templates, assets).
*   **NFR-03: Usability:**
    *   The user interface should be intuitive and require minimal training for marketing professionals.
    *   Workflow should be clear and guide the user through the generation process.
    *   Error messages should be clear and helpful.
*   **NFR-04: Reliability:**
    *   The platform should aim for high availability (e.g., 99.5% uptime).
    *   Robust error handling for external API calls (Azure OpenAI, ComfyUI).
    *   Regular data backups.
*   **NFR-05: Security:**
    *   Secure user authentication and session management.
    *   Protection against common web vulnerabilities (OWASP Top 10).
    *   Secure handling of API keys.
    *   Access control for user data and assets.
*   **NFR-06: Maintainability:**
    *   Code should follow best practices for Flask and React.
    *   Modular design to facilitate updates and feature additions.
    *   Adequate logging and monitoring.

## 7. Technical Stack (Confirmed & Proposed)

*   **Backend:** Flask (Python)
*   **Frontend:** React (JavaScript/TypeScript)
*   **LLM:** Azure OpenAI API
*   **Image Generation:** ComfyUI
*   **Database:** PostgreSQL
*   **Job Queue:** Celery with Redis or RabbitMQ (Recommended)
*   **Caching:** Redis (Recommended)

## 8. Infrastructure Requirements

*   **Application Server:** Linux environment suitable for Python/Flask and Node.js/React builds. Specs TBD (e.g., 2-4 vCPU, 4-8 GB RAM, 50GB SSD initially, subject to load testing). Requires Python, Node.js, pip, npm/yarn.
*   **ComfyUI Server(s):** Separate instance(s) with GPU(s) suitable for Stable Diffusion models. Managed by the dedicated dev team. Requires network connectivity with the application server.
*   **Database Server:** Dependent on chosen DB technology.
*   **Queue/Cache Server:** Dependent on chosen technology (e.g., Redis server).
*   **Deployment:** Docker containers. CI/CD pipeline recommended.

## 9. Open Questions / Future Considerations

*   Define specific LORA storage limits and management details with Ops team.
*   Detail User roles and team management features (FR-01, FR-06.3).
*   Finalize Monitoring, logging, and alerting strategy.
*   Develop Cost estimation and optimization plan for API usage (Azure, ComfyUI hosting).
*   (Future) Potential for A/B testing generated ads directly via the platform.
* Optimize PSD files manipulation (For auto captioning the generated images)
