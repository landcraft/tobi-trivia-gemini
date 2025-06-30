from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
# Import the Google Generative AI client library
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

# Configure the Gemini API key from environment variables
# IMPORTANT: Never hardcode your API key directly in code.
# For production, set this environment variable securely.
GEMINI_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Placeholder for Supabase configuration
# SUPABASE_URL = os.environ.get('SUPABASE_URL')
# SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY environment variable not set. LLM calls will fail.")

@app.route('/')
def hello_world():
    return 'Tobi Trivia Backend is running! This is where your LLM and Supabase magic happens.'

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
            # Pass the schema directly as a Python dict for structured output
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

        # Parse the JSON response from the LLM
        # The LLM's response.text is already a JSON string because of response_mime_type
        generated_questions = json.loads(response.text)

        # --- Supabase Integration (Future Enhancement) ---
        # Here, you would integrate with Supabase:
        # 1. Fetch recent questions from Supabase to ensure no repeats (beyond in-session history).
        #    Example:
        #    from supabase import create_client, Client
        #    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        #    response = supabase.table('trivia_questions').select('question_text').execute()
        #    existing_questions = [item['question_text'] for item in response.data]
        # 2. Filter `generated_questions` against the Supabase history.
        # 3. Store the new, unique questions in your Supabase database.
        #    Example:
        #    for q in generated_questions:
        #        supabase.table('trivia_questions').insert({"question_text": q['question'], "answer_text": q['correctAnswerKey']}).execute()
        # For now, we return the LLM's output directly.

        return jsonify(generated_questions)

    except Exception as e:
        print(f"Error generating trivia: {e}")
        return jsonify({"error": f"Failed to generate trivia: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Run Flask app on port 5000
