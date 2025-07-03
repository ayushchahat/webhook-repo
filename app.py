from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# ✅ MongoDB connection string (consider using os.getenv for production)
client = MongoClient("mongodb+srv://ayush110903kumar:88NfaDi2WSDljsm1@cluster0.wsofxhq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["webhook_db"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    data = request.json

    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    # Initialize schema with safe defaults
    event = {
        "request_id": "N/A",
        "author": data.get("sender", {}).get("login", "unknown"),
        "action": "N/A",
        "from_branch": "-",
        "to_branch": "-",
        "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    }

    # ✅ Handle push events
    if event_type == "push":
        event["action"] = "PUSH"
        event["request_id"] = data.get("head_commit", {}).get("id", "N/A")
        event["from_branch"] = data.get("ref", "").split("/")[-1]
        event["to_branch"] = "main"  # assumption

    # ✅ Handle pull request events
    elif event_type == "pull_request":
        pr = data.get("pull_request", {})
        action = data.get("action", "")

        event["request_id"] = str(pr.get("id", "N/A"))
        event["from_branch"] = pr.get("head", {}).get("ref", "-")
        event["to_branch"] = pr.get("base", {}).get("ref", "-")

        if action == "opened":
            event["action"] = "PULL_REQUEST"
        elif action == "closed" and pr.get("merged"):
            event["action"] = "MERGE"
        else:
            return jsonify({"message": "PR event ignored"}), 200

    else:
        return jsonify({"message": f"{event_type} not handled"}), 200

    collection.insert_one(event)
    return jsonify({"status": "stored"}), 201

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return jsonify(events)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
