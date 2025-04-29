from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import load_faq, find_answer, generate_schedule

app = Flask(__name__)
CORS(app)

# Load the FAQ data once when the server starts
faq_data = load_faq()
last_question_type = {"pending_schedule": False}

@app.route('/')
def home():
    return "AskHusky backend is running!"

@app.route('/ask', methods=['POST'])
def ask():
    global last_question_type
    user_input = request.json.get("question", "").lower().strip()

    if last_question_type["pending_schedule"]:
        if user_input in ["freshman", "sophomore", "junior", "senior"]:
            last_question_type["pending_schedule"] = False
            return jsonify({"answer": generate_schedule(user_input)})
        else:
            return jsonify({"answer": "Please reply with one of: Freshman, Sophomore, Junior, or Senior."})

    answer = find_answer(user_input, faq_data)

    if "Which year are you in?" in answer:
        last_question_type["pending_schedule"] = True

    return jsonify({"answer": answer})

if __name__ == '__main__':
    # Host 0.0.0.0 allows access on Render; port 5000 is standard
    app.run(host='0.0.0.0', port=5000)
