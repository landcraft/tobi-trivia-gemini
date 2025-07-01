from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
import os
import json
import google.generativeai as genai

# Determine the absolute path to the 'dist' folder
# BASE_DIR will be /app/backend (due to WORKDIR /app and FLASK_APP backend/app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DIST_DIR will be /app/dist (one level up from backend, then into dist)
DIST_DIR = os.path.join(os.path.dirname(BASE_DIR), 'dist')

app = Flask(
    __name__,
    # Flask's default static_url_path is '/static'.
    # We need to point static_folder to where React's static assets are: /app/dist/static
    static_folder=os.path.join(DIST_DIR, 'static'),
    # Flask's template_folder is where render_template looks for files.
    # index.html is directly in /app/dist.
    template_folder=DIST_DIR
)
CORS(app) # Enable CORS for frontend communication

# Configure the Gemini API key from environment variables
GEMINI_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Placeholder for Supabase configuration
# SUPABASE_URL = os.environ.get('SUPABASE_URL')
# SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY environment variable not set. LLM calls will fail.")

# Route to serve the frontend's index.html for the root path
@app.route('/')
def serve_index():
    # Flask will look for index.html in the 'template_folder' (which is /app/dist)
    return render_template('index.html')

# Route to serve React's bundled static files (CSS, JS, etc. located in /static/)
# This route specifically handles requests like /static/css/main.css or /static/js/main.js
@app.route('/static/<path:filename>')
def serve_react_static(filename):
    # send_from_directory will serve files from app.static_folder (which is /app/dist/static)
    # The 'filename' will be like 'css/main.css' or 'js/main.js'
    return send_from_directory(app.static_folder, filename)

# Route to serve other root-level static files (like manifest.json, favicon.ico)
# and also act as a fallback for React Router paths
@app.route('/<path:filename>')
def serve_other_root_static(filename):
    # Check if the requested file exists directly in the DIST_DIR (e.g., manifest.json)
    if os.path.exists(os.path.join(DIST_DIR, filename)):
        return send_from_directory(DIST_DIR, filename)
    # If not a direct file, and not the root path, then it's likely a React Router path
    # or an asset not found. In a SPA, we usually serve index.html for these.
    return render_template('index.html')


@app.route('/generate_trivia', methods=['POST'])
def generate_trivia():
    """
    This endpoint securely calls the LLM and will handle Supabase interaction.
    """
    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API key not configured on backend. Please set GOOGLE_API_KEY environment variable."}), 500

    data = request.get_json()
    prompt_content = data.get('prompt', '')

    if not prompt_content:
        return jsonify({"error": "No prompt content received from frontend."}), 400

    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Make the LLM call with the prompt received from the frontend
        # Removed 'response_schema' as it's not supported directly by generate_content for this model
        response = model.generate_content(
            prompt_content,
            generation_config={
                "response_mime_type": "application/json",
            }
        )

        # The LLM is instructed to return JSON as text, so we parse it here.
        # Ensure the LLM's response.text is a valid JSON string.
        generated_questions = json.loads(response.text)

        # --- Supabase Integration (Future Enhancement) ---
        # Here, you would integrate with Supabase:
        # from supabase import create_client, Client
        # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # response = supabase.table('trivia_questions').select('question_text').execute()
        # existing_questions = [item['question_text'] for item in response.data]
        # Filter `generated_questions` against the Supabase history.
        # Store the new, unique questions in your Supabase database.
        # For now, we return the LLM's output directly.

        return jsonify(generated_questions)

    except json.JSONDecodeError as e:
        print(f"Error parsing LLM response as JSON: {e}")
        print(f"LLM raw response: {response.text if 'response' in locals() else 'No response object'}")
        return jsonify({"error": f"Failed to parse LLM response as JSON. Please try again. ({str(e)})"}), 500
    except Exception as e:
        print(f"Error generating trivia: {e}")
        return jsonify({"error": f"Failed to generate trivia: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
