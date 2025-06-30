from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
import os
import json

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

# IMPORTANT: In a real application, your LLM API key and Supabase client
# would be initialized here using environment variables.
# For this example, we're simulating the LLM call that the frontend currently makes.

@app.route('/')
def hello_world():
    return 'Tobi Trivia Backend is running! This is where your LLM and Supabase magic happens.'

@app.route('/generate_trivia', methods=['POST'])
def generate_trivia():
    """
    This endpoint would securely call the LLM and interact with Supabase.
    The frontend will send the prompt content from LLM.
    """
    data = request.get_json()
    prompt_content = data.get('prompt', '')

    # --- SIMULATED LLM CALL AND SUPABASE INTERACTION ---
    # In a real scenario:
    # 1. You'd use a secure LLM client library (e.g., Google's Python client)
    # 2. Your actual LLM API key would be read from an environment variable (e.g., os.environ.get('GOOGLE_API_KEY'))
    # 3. You'd implement web scraping here if needed.
    # 4. You'd use the Supabase Python client to:
    #    - Fetch recent questions for repeat prevention.
    #    - Store the newly generated unique questions.
    #    - This ensures question history persists across sessions and is secure.

    # For demonstration, we'll echo a fixed structure or simulate a very basic LLM response
    # based on the frontend's prompt request.
    print(f"Backend received request for trivia generation with prompt:\n{prompt_content[:200]}...") # Print first 200 chars

    # This is a placeholder response that mimics what the LLM *would* return
    # if called from here. The frontend is still making the direct LLM call for now.
    # You would replace this with actual LLM API call and Supabase logic.
    mock_questions = [
        {
            "question": "What is 10 plus 15?",
            "options": [
                {"key": "A", "text": "20"},
                {"key": "B", "text": "25"},
                {"key": "C", "text": "30"},
                {"key": "D", "text": "15"}
            ],
            "correctAnswerKey": "B"
        },
        {
            "question": "Which planet is known for its beautiful rings?",
            "options": [
                {"key": "A", "text": "Mars"},
                {"key": "B", "text": "Jupiter"},
                {"key": "C", "text": "Saturn"},
                {"key": "D", "text": "Neptune"}
            ],
            "correctAnswerKey": "C"
        },
        {
            "question": "Who is the main character in the 'Dog Man' book series?",
            "options": [
                {"key": "A", "text": "Captain Underpants"},
                {"key": "B", "text": "Dog Man"},
                {"key": "C", "text": "Petey the Cat"},
                {"key": "D", "text": "Lil' Petey"}
            ],
            "correctAnswerKey": "B"
        },
        {
            "question": "If you have 3 apples and eat 1, how many do you have left?",
            "options": [
                {"key": "A", "text": "4"},
                {"key": "B", "text": "3"},
                {"key": "C", "text": "2"},
                {"key": "D", "text": "1"}
            ],
            "correctAnswerKey": "C"
        },
        {
            "question": "What is the largest organ in the human body?",
            "options": [
                {"key": "A", "text": "Brain"},
                {"key": "B", "text": "Heart"},
                {"key": "C", "text": "Skin"},
                {"key": "D", "text": "Lungs"}
            ],
            "correctAnswerKey": "C"
        },
        {
            "question": "How many minutes are in half an hour?",
            "options": [
                {"key": "A", "text": "15"},
                {"key": "B", "text": "30"},
                {"key": "C", "text": "45"},
                {"key": "D", "text": "60"}
            ],
            "correctAnswerKey": "B"
        },
        {
            "question": "What type of creature is Pikachu from Pokémon?",
            "options": [
                {"key": "A", "text": "Fire type"},
                {"key": "B", "text": "Water type"},
                {"key": "C", "text": "Electric type"},
                {"key": "D", "text": "Grass type"}
            ],
            "correctAnswerKey": "C"
        },
        {
            "question": "Which planet is closest to the Sun?",
            "options": [
                {"key": "A", "text": "Venus"},
                {"key": "B", "text": "Earth"},
                {"key": "C", "text": "Mars"},
                {"key": "D", "text": "Mercury"}
            ],
            "correctAnswerKey": "D"
        },
        {
            "question": "What do plants need to make their own food?",
            "options": [
                {"key": "A", "text": "Sugar, water, air"},
                {"key": "B", "text": "Sunlight, water, carbon dioxide"},
                {"key": "C", "D": "Soil, water, fertilizer"},
                {"key": "D", "text": "Dirt, rocks, light"}
            ],
            "correctAnswerKey": "B"
        },
        {
            "question": "Who writes in a diary in the 'Diary of a Wimpy Kid' series?",
            "options": [
                {"key": "A", "text": "Rodrick Heffley"},
                {"key": "B", "text": "Manny Heffley"},
                {"key": "C", "text": "Greg Heffley"},
                {"key": "D", "text": "Rowley Jefferson"}
            ],
            "correctAnswerKey": "C"
        }
    ]

    return jsonify(mock_questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Run Flask app on port 5000
