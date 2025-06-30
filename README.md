# Tobi's Daily Trivia

Welcome to Tobi's Daily Trivia, an engaging and humorous multiple-choice quiz application designed for 7-10 year olds! This project is set up to be self-hostable using Docker and can be published to GitHub Container Registry (GHCR).

## Features

* **Engaging UI:** Colorful and child-friendly design.
* **Multiple Choice Quiz:** Interactive questions with four options.
* **Instant Feedback:** Immediate indication of correct/incorrect answers.
* **Score Tracking:** Tracks the player's score throughout the quiz.
* **Quiz Results:** Displays a summary of the final score after 10 questions.
* **New Questions Button:** Fetches a fresh set of 10 trivia questions (via secure backend LLM call).
* **Topic Focus:** Questions are sourced with a focus on maths, science, space, and popular children's literature, relevant for UK, Europe, or US audiences.
* **Dockerized:** Ready for containerized deployment.
* **Multi-Architecture Docker Images:** Built for `amd64` and `arm64` via GitHub Actions.
* **Secure API Key Handling:** LLM API key managed securely on the backend via environment variables.

## Project Structure

```
tobi-trivia-app/
├── .github/                     # GitHub Actions workflows
│   └── workflows/
│       └── docker-build.yml     # Workflow to build and push Docker images
├── backend/                     # Python Flask backend (Handles secure API calls and DB)
│   ├── app.py                   # Flask application (LLM integration, Supabase placeholder)
│   ├── requirements.txt         # Python dependencies (Flask, Flask-Cors, google-generativeai)
│   └── Dockerfile.backend       # Dockerfile for backend service
├── frontend/                    # ReactJS frontend application
│   ├── public/                  # Static assets for React app
│   │   └── index.html
│   ├── src/                     # React source code
│   │   ├── App.js               # Main React component for the quiz
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Tailwind CSS imports
│   ├── nginx.conf               # Nginx configuration for serving the React app
│   ├── package.json             # Node.js dependencies and scripts
│   ├── postcss.config.js        # PostCSS configuration for Tailwind
│   ├── tailwind.config.js       # Tailwind CSS configuration
│   └── Dockerfile.frontend      # Dockerfile for frontend service (Nginx)
├── docker-compose.yml           # Docker Compose file to orchestrate services
└── README.md                    # This README file
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
    In the root of your `tobi-trivia-app` directory, create a file named `.env` and add your API keys and Supabase URLs:

    ```dotenv
    # .env
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL" # Placeholder for future Supabase integration
    SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"   # Placeholder for future Supabase integration
    ```
    **IMPORTANT:** Replace the placeholder values with your actual Gemini API key and (if applicable) Supabase credentials. Do NOT commit this `.env` file to your Git repository.

3.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will:
    * Build the `frontend` image (builds the React app and sets up Nginx).
    * Build the `backend` image (installs Python dependencies and runs the Flask app).
    * Start both containers, passing the environment variables from your `.env` file to the `backend` service.

4.  **Access the application:**
    Open your web browser and navigate to `http://localhost`.

    The backend API will be available at `http://localhost:5000`.

## Deployment to GitHub Container Registry (GHCR)

This repository is configured with GitHub Actions to automatically build and push multi-architecture Docker images to GHCR.

1.  **Create a GitHub Repository:**
    * Go to GitHub and create a new public repository (e.g., `tobi-trivia-app`).
    * **Do NOT** initialize it with a README or `.gitignore`.

2.  **Set GitHub Secrets:**
    * Go to your GitHub repository -> `Settings` -> `Secrets and variables` -> `Actions`.
    * Click `New repository secret` and add the following secrets:
        * `GOOGLE_API_KEY`: Your actual Gemini API key.
        * `SUPABASE_URL`: Your Supabase project URL (if integrating Supabase).
        * `SUPABASE_KEY`: Your Supabase anon key (if integrating Supabase).

3.  **Push Your Code:**
    * Navigate to the root of your local `tobi-trivia-app` directory in your terminal.
    * Initialize a Git repository (if you haven't already):
        ```bash
        git init
        git add .
        git commit -m "Initial commit of Tobi's Daily Trivia App with Docker setup"
        ```
    * Connect your local repository to your GitHub repository:
        ```bash
        git remote add origin [https://github.com/YOUR_USERNAME/tobi-trivia-app.git](https://github.com/YOUR_USERNAME/tobi-trivia-app.git)
        git branch -M main
        git push -u origin main
        ```
        (Replace `YOUR_USERNAME` and `tobi-trivia-app` with your actual GitHub username and repository name).

4.  **Monitor GitHub Actions:**
    * Once you push to `main` or create a new GitHub Release, the `docker-build.yml` workflow will automatically trigger.
    * Go to the "Actions" tab in your GitHub repository to monitor the build progress.
    * Upon successful completion, your Docker images will be available in your GitHub Package Registry (GHCR) under the "Packages" tab of your GitHub profile/repository.

### Pulling Docker Images from GHCR

GitHub users can pull your images using the `docker pull` command. The image names will follow this format:

* **Frontend:** `ghcr.io/YOUR_USERNAME/YOUR_REPOSITORY_NAME/frontend:latest` (or a specific tag/commit SHA)
* **Backend:** `ghcr.io/YOUR_USERNAME/YOUR_REPOSITORY_NAME/backend:latest` (or a specific tag/commit SHA)

Example:
```bash
docker pull ghcr.io/your-username/tobi-trivia-app/frontend:latest
docker pull ghcr.io/your-username/tobi-trivia-app/backend:latest
```

Users can then use your `docker-compose.yml` (modified to pull images instead of build them) to run the application.

## Future Enhancements (Backend Implementation)

To make "Tobi's Daily Trivia" truly robust and secure, the next steps involve implementing the full backend logic:

* **LLM Integration:** The `backend/app.py` now includes the `google-generativeai` library and reads the API key from environment variables. You can further refine prompts or add more complex LLM interactions here.
* **Supabase Database:**
    * Set up a Supabase project and create a `trivia_questions` table.
    * Uncomment `supabase` in `backend/requirements.txt`.
    * Use the `supabase-py` client library in `backend/app.py` to:
        * Store new questions generated by the LLM.
        * Retrieve questions for the quiz, implementing robust repeat prevention logic (e.g., fetching questions not seen in the last 5 days or 5 quiz runs per user, possibly per user ID if you add authentication).
        * Handle user data (if you expand to user-specific scores or question history).
* **Web Scraping:** If desired, implement web scraping using libraries like `requests` and `BeautifulSoup` in the backend to gather trivia from free online sources, then feed this data to the LLM or directly into Supabase.

Enjoy building and sharing Tobi's Daily Trivia!
