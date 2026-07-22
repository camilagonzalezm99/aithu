import random

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Store conversation history for multi-turn conversations
conversation_history = []


def load_prompt():
    """Load the prompt from prompt.txt file."""
    try:
        with open("prompt.txt", "r") as file:
            prompt = file.read().strip()
            return "" if prompt == "You are a marketing assistant" else prompt
    except FileNotFoundError:
        return ""


def load_knowledge_base():
    """Load local Q&A knowledge from the marketing strategies file."""
    try:
        with open("marketing_strategies.txt", "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return [
            "Marketing Strategies",
            "Ask about financial goals and recommend suitable credit cards.",
            "Explain benefits, annual fees, intro offers, and eligibility requirements.",
        ]


def find_answer(user_message):
    """Return a simple local Q&A answer based on the knowledge file."""
    message = user_message.lower()
    knowledge = load_knowledge_base()

    if "display marketing strategies" in message:
        try:
            with open("marketing_strategies.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Marketing strategies file not found."

    if "greet" in message or "hello" in message or "hi" in message:
        return "Hello! I can help answer questions about marketing strategies and customer guidance."

    for item in knowledge:
        lowered_item = item.lower()
        if any(keyword in message for keyword in ["goal", "financial", "credit card", "spending", "travel", "cashback", "rewards", "low interest", "annual fee", "promo", "eligibility", "follow up", "application"]):
            if any(keyword in lowered_item for keyword in ["financial goals", "credit cards", "spending habits", "travel", "cashback", "rewards", "low interest", "annual fees", "promotions", "eligibility", "follow up", "application assistance"]):
                return item

    if "marketing" in message:
        return "The knowledge base focuses on professional client greetings, recommending appropriate credit cards, explaining fees and offers, and following up with interested clients."

    return "I can answer questions based on the available marketing strategy knowledge. Try asking about credit card recommendations, fees, promotions, or follow-up steps."


def get_simulator_question():
    """Return a question for simulator mode."""
    questions = [
        "What are your financial goals?",
        "Do you prefer travel rewards, cashback, or low-interest benefits?",
        "Are you interested in card features like annual fees, introductory offers, or eligibility requirements?",
        "Would you like help comparing credit card options based on your spending habits?",
    ]
    return random.choice(questions)


def get_qna_response(user_message, simulator_mode=False):
    """Build a local Q&A chatbot response without external APIs."""
    conversation_history.append({"role": "user", "content": user_message})

    system_prompt = load_prompt()
    assistant_message = get_simulator_question() if simulator_mode else find_answer(user_message)

    if system_prompt:
        assistant_message = f"{system_prompt}\n\n{assistant_message}"

    conversation_history.append({"role": "assistant", "content": assistant_message})
    return assistant_message


@app.route('/')
def index():
    prompt = load_prompt()
    return render_template('index.html', prompt=prompt)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    simulator_mode = bool(data.get('simulator_mode', False))

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    bot_response = get_qna_response(user_message, simulator_mode=simulator_mode)
    return jsonify({'response': bot_response})


@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history."""
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'cleared'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
