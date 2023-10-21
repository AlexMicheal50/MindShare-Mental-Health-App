from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name)

# Load values from the .env file if it exists
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("API_SECRET_KEY")

INSTRUCTIONS = """You are a friend and companion, and you speak in a positive and affirmative way. You are like a therapist and help make the user feel better by telling beautiful stories and quotes to help the person feel better. If you are asked for something irrelevant or an error, you should respond with 'I am sorry sweetheart, I love you too much and cannot do that to you.'"""

TEMPERATURE = 0.7
MAX_TOKENS = 370
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

def get_response(instructions, user_message):
    # Build the messages
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": user_message}
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )

    return completion.choices[0].message.content

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('userMessage')
    response = get_response(INSTRUCTIONS, user_message)
    return jsonify({'chatgptResponse': response})

if __name__ == "__main__":
    app.run(debug=True)
