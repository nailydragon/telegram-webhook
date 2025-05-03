from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def classify_message():
    data = request.get_json()
    message = data.get("message", "").lower()

    # Default values
    category = "info"
    is_important = False
    is_urgent = False

    # Rules for classification
    if any(word in message for word in ["server down", "404", "otp", "not working", "fail", "withdraw problem", "error", "verify fail", "mismatch", "crash"]):
        category = "bug"
        is_important = True
        is_urgent = True
    elif any(word in message for word in ["please", "add", "remove", "update", "need to", "can you", "want"]):
        category = "request"
        is_important = True
        is_urgent = "now" in message or "urgent" in message
    elif any(word in message for word in ["how", "what", "can i", "where", "why"]):
        category = "query"
        is_important = False
        is_urgent = False
    elif any(word in message for word in ["info", "just for your info", "fyi", "announcement"]):
        category = "info"
        is_important = False
        is_urgent = False
    else:
        # Fallback if unknown but seems serious
        if "admin" in message and "not sync" in message:
            category = "bug"
            is_important = True
            is_urgent = True

    return jsonify({
        "category": category,
        "is_important": is_important,
        "is_urgent": is_urgent
    })

if __name__ == '__main__':
    app.run(debug=True)
