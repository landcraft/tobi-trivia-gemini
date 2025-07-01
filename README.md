# Tobi's Daily Trivia

Welcome to Tobi's Daily Trivia, an engaging and humorous multiple-choice quiz application designed for 7-10 year olds! This project is set up to be self-hostable using a single Docker image and can be published to GitHub Container Registry (GHCR).

## Features

* **Engaging UI:** Colorful and child-friendly design.
* **Multiple Choice Quiz:** Interactive questions with four options.
* **Instant Feedback:** Immediate indication of correct/incorrect answers.
* **Score Tracking:** Tracks the player's score throughout the quiz.
* **Quiz Results:** Displays a summary of the final score after 10 questions.
* **New Questions Button:** Fetches a fresh set of 10 trivia questions (via secure backend LLM call).
* **Topic Focus:** Questions are sourced with a focus on maths, science, space, and popular children's literature, relevant for UK, UK, or US audiences.
* **Single Docker Image:** Frontend and backend are combined into one streamlined Docker image.
* **Multi-Architecture Docker Images:** Built for `amd64` and `arm64` via GitHub Actions.
* **Secure API Key Handling:** LLM API key managed securely on the backend via environment variables.

## Project Structure

```
tobi-trivia-app/
├── .github/                     # GitHub Actions workflows
│   └── workflows/
│       └── docker-build.yml     # Workflow to build and push Docker images (updated)
├── backend/                     # Python Flask backend (Handles secure API calls and DB)
│   ├── app.py                   # Flask application (now also serves frontend static files)
│   └── requirements.txt         # Python dependencies (Flask, Flask-Cors, google-generativeai)
├── frontend/                    # ReactJS frontend application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js               # Main React component for the quiz (updated for relative API path)
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json             # Node.js dependencies and scripts
│   ├── postcss.config.js        # PostCSS configuration for Tailwind
│   └── tailwind.config.js       # Tailwind CSS configuration
├── Dockerfile                   # NEW: Combined Dockerfile for frontend and backend
├── docker-compose.yml           # Docker Compose file to orchestrate the single service (updated)
└── README.md                    # This README file (updated)
```

## Getting Started

### Prerequisites

* Docker Desktop (includes Docker Engine and Docker Compose)
* Git
* Node.js & npm (for local frontend development/testing, though not strictly needed to run via Docker)

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/tobi-trivia-app.git](https://github.com/your-username/tobi-trivia-app.git)
    cd tobi-trivia-app
    ```
    (Replace `your-username/tobi-trivia-app` with your actual repository path after you've pushed it to GitHub).

2.  **Create a `.env` file:**
    In the root of your `tobi-trivia-app` directory, create a file named `.env` and add your environment variables:

    ```dotenv
    # .env
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```
    **IMPORTANT:** Replace the placeholder value with your actual Gemini API key. Do NOT commit this `.env` file to your Git repository.

3.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will:
    * Build the single `tobi-trivia-app` image (builds React, then Flask, and copies React assets into Flask's static/templates folders).
    * Start the combined container, passing the environment variables from your `.env` file to the Flask application.

4.  **Access the application:**
    Open your web browser and navigate to `http://localhost`.

    The combined application (frontend and backend API) will be available on port 80.

### About the "Development Server" Warning

You might see a warning in your Docker logs like: "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead." This is a standard message from Flask. Flask's built-in server is lightweight and convenient for development, but it's not designed for the demands of a production environment (e.g., handling many concurrent requests, security, stability). For a real-world, high-traffic deployment, you would typically use a production-ready WSGI (Web Server Gateway Interface) server like [Gunicorn](https://gunicorn.org/) or [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) to run your Flask application. For this self-hostable example, the development server is sufficient, but keep this in mind for a scaled production setup.

## How it Works

This application, "Tobi's Daily Trivia," works by combining a React frontend with a Flask backend, all packaged neatly within a single Docker container for easy deployment. Here's a breakdown of how it functions:

### 1. The Frontend (React - `frontend/src/App.js`)

* **User Interface:** This is what you see in your browser. It displays the trivia questions, options, handles user selections, provides immediate feedback (correct/incorrect), tracks the score, and shows the final results.
* **Requesting Questions:** When the page loads initially or when you click the "New Questions" button, the React frontend makes an asynchronous request to the backend. It constructs a detailed `prompt` string that instructs the Gemini LLM on what kind of trivia questions to generate (e.g., number of questions, topics, target audience, and the desired JSON output format).
* **Displaying Data:** Once the frontend receives a successful response from the backend (which contains the generated trivia questions in JSON format), it updates its state to display the questions one by one.

### 2. The Backend (Flask - `backend/app.py`)

* **Serving the Frontend:** The Flask application acts as the web server for both the frontend and the API. When you access `http://localhost` (or your deployed URL), Flask serves the `index.html` file (and its associated CSS/JavaScript bundles) from the React build output.
    * `static_folder=os.path.join(DIST_DIR, 'static')`: This tells Flask to look for React's bundled CSS and JS files (which are typically in a `static/` subdirectory within React's build) in the `dist/static` folder inside the Docker container.
    * `template_folder=DIST_DIR`: This tells Flask to find `index.html` (the main entry point for the React app) directly in the `dist` folder.
    * `@app.route('/static/<path:filename>')` and `@app.route('/<path:filename>')`: These routes ensure that all necessary static assets (like `main.css`, `main.js`, `manifest.json`, and even React Router paths) are correctly served to the browser.
* **LLM API Endpoint (`/generate_trivia`):** This is the core logic for question generation.
    * The frontend sends its `prompt` to this endpoint.
    * The Flask backend then securely initializes the `google.generativeai` client using your `GOOGLE_API_KEY` (which is passed as an environment variable to the Docker container, keeping it out of client-side code).
    * It calls `model.generate_content(prompt_content, generation_config={"response_mime_type": "application/json"})`. This sends the detailed prompt to the Gemini 2.0 Flash model and requests the response in JSON format.
    * The raw text response from Gemini is then parsed as JSON using `json.loads()`.
    * Finally, the parsed JSON (the list of trivia questions) is sent back to the frontend.
* **Error Handling:** The backend includes `try-except` blocks to catch potential errors during the LLM call or JSON parsing, providing informative messages back to the frontend.

### 3. Containerization (Docker and Docker Compose)

* **`Dockerfile`:** This file acts as a blueprint for building your single Docker image.
    * **Multi-stage build:** It first uses a `node:18-alpine` image to build the React frontend (`npm run build`). This creates a `build` directory containing all the optimized HTML, CSS, and JavaScript.
    * Then, it switches to a `python:3.9-slim-buster` image for the backend.
    * It copies the Python dependencies (`requirements.txt`) and the Flask application (`app.py`).
    * Crucially, it copies the *built* React frontend from the first stage into a `/dist` directory within the Python image.
    * It exposes port 5000, which is where the Flask app will run inside the container.
    * The `CMD ["python", "./backend/app.py"]` instruction tells Docker to run your Flask application when the container starts.
* **`docker-compose.yml`:** This file simplifies running your Dockerized application.
    * It defines a single service named `tobi-trivia-app`.
    * The `build` section tells Docker Compose to build the image using the `Dockerfile` in the current directory.
    * `ports: - "80:5000"` maps port 80 on your host machine to port 5000 inside the container. This means you can access the application by navigating to `http://localhost` in your browser.
    * `environment:` section passes your `GOOGLE_API_KEY` from your local `.env` file (or GitHub Secrets during deployment) into the container, making it available to your Flask backend.

## Deployment to GitHub Container Registry (GHCR)

This repository is configured with GitHub Actions to automatically build and push a single multi-architecture Docker image to GHCR.

1.  **Create a GitHub Repository:**
    * Go to GitHub and create a new public repository (e.g., `tobi-trivia-app`).
    * **Do NOT** initialize it with a README or `.gitignore`.

2.  **Set GitHub Secrets:**
    * Go to your GitHub repository -> `Settings` -> `Secrets and variables` -> `Actions`.
    * Click `New repository secret` and add the following secret:
        * `GOOGLE_API_KEY`: Your actual Gemini API key.

3.  **Push Your Code:**
    * Navigate to the root of your local `tobi-trivia-app` directory in your terminal.
    * Initialize a Git repository (if you haven't already):
        ```bash
        git init
        git add .
        git commit -m "Initial commit of Tobi's Daily Trivia App with single Docker image setup"
        ```
    * Connect your local repository to your GitHub repository:
        ```bash
        git remote add origin [https://github.com/your-username/tobi-trivia-app.git](https://github.com/your-username/tobi-trivia-app.git)
        git branch -M main
        git push -u origin main
        ```
        (Replace `your-username` and `tobi-trivia-app` with your actual GitHub username and repository name).

4.  **Monitor GitHub Actions:**
    * Once you push to `main` or create a new GitHub Release, the `docker-build.yml` workflow will automatically trigger.
    * Go to the "Actions" tab in your GitHub repository to monitor the build progress.
    * Upon successful completion, your Docker image will be available in your GitHub Package Registry (GHCR) under the "Packages" tab of your GitHub profile/repository.

### Pulling and Running the Combined Docker Image from GHCR

Once the Docker image is published to GHCR, other users (or you on a different machine) can pull and run it without needing to build it from source.

1.  **Pull the Docker Image:**
    ```bash
    docker pull ghcr.io/YOUR_USERNAME/tobi-trivia-app:latest
    ```
    (Replace `YOUR_USERNAME` and `tobi-trivia-app` with your actual GitHub username and repository name).

2.  **Create a `.env` file for deployment:**
    In the directory where you want to run the application, create a `.env` file with your environment variables (as described in "Local Development Setup" step 2).

3.  **Create a `docker-compose.yml` for deployment:**
    Create a `docker-compose.yml` file in the same directory. This version uses `image:` instead of `build:` to pull the pre-built combined image.

    ```yaml
    # docker-compose.yml (for running pre-built combined image from GHCR)
    version: '3.8'

    services:
      tobi-trivia-app:
        image: ghcr.io/YOUR_USERNAME/tobi-trivia-app:latest # Replace YOUR_USERNAME and tobi-trivia-app
        ports:
          - "80:5000" # Map host port 80 to container port 5000 (where Flask runs)
        environment:
          # These variables will be read from your .env file
          GOOGLE_API_KEY: ${GOOGLE_API_KEY}
        restart: unless-stopped
    ```
    (Remember to replace `YOUR_USERNAME` and `tobi-trivia-app` in the `image:` line).

4.  **Run the application:**
    ```bash
    docker-compose up -d
    ```
    This will start the single combined service.

5.  **Access the application:**
    Open your web browser and navigate to `http://localhost`.

## Future Enhancements (Backend Implementation)

To make "Tobi's Daily Trivia" truly robust and secure, the next steps involve implementing the full backend logic:

* **Database Integration:** If you need to persist questions or user data, consider adding a database.
* **Web Scraping:** If desired, implement web scraping using libraries like `requests` and `BeautifulSoup` in the backend to gather trivia from free online sources, then feed this data to the LLM or directly into a database.

Enjoy building and sharing Tobi's Daily Trivia!
