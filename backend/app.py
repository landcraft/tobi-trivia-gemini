from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
import os
import json
import google.generativeai as genai

# Initialize Flask app, configuring static and template folders relative to the app's root_path
# When FLASK_APP=backend/app.py and WORKDIR /app, Flask's root_path becomes /app/backend.
# So, static and templates folders should be referenced directly by their names within that root.
app = Flask(
    __name__,
    static_folder='static',    # Corrected path: refers to /app/backend/static
    template_folder='templates' # Corrected path: refers to /app/backend/templates
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
    # Flask will look for index.html in the 'templates' folder
    return render_template('index.html')

# Route to serve static files (CSS, JS, images from React build)
# This route catches any requests for files not explicitly handled by other routes
# and attempts to serve them from the static folder.
@app.route('/<path:filename>')
def serve_static(filename):
    # Flask will look for these files in the 'static' folder
    return send_from_directory(app.static_folder, filename)

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
        response = model.generate_content(
            prompt_content,
            generation_config={
                "response_mime_type": "application/json",
            },
            response_schema={
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "question": { "type": "STRING" },
                        "options": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "key": { "type": "STRING" },
                                    "text": { "type": "STRING" }
                                }
                            }
                        },
                        "correctAnswerKey": { "type": "STRING" }
                    }
                }
            }
        )

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

    except Exception as e:
        print(f"Error generating trivia: {e}")
        return jsonify({"error": f"Failed to generate trivia: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
