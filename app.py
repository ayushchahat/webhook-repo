from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# ⛔ Replace this URI with your actual MongoDB Atlas connection string
client = MongoClient("mongodb+srv://ayush110903kumar:88NfaDi2WSDljsm1@cluster0.wsofxhq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


db = client["webhook_db"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    data = request.json

    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    event = {
        "event_type": event_type,
        "author": data.get("sender", {}).get("login", "unknown"),
        "timestamp": datetime.utcnow()
    }

    if event_type == "push":
        event["to_branch"] = data["ref"].split("/")[-1]
        event["message"] = f'{event["author"]} pushed to {event["to_branch"]}'

    elif event_type == "pull_request":
        pr = data["pull_request"]
        from_branch = pr["head"]["ref"]
        to_branch = pr["base"]["ref"]
        action = data.get("action")
        if action == "opened":
            event["from_branch"] = from_branch
            event["to_branch"] = to_branch
            event["message"] = f'{event["author"]} submitted a pull request from {from_branch} to {to_branch}'
        elif action == "closed" and pr.get("merged"):
            event["from_branch"] = from_branch
            event["to_branch"] = to_branch
            event["message"] = f'{event["author"]} merged branch {from_branch} to {to_branch}'

    else:
        event["message"] = f"{event['author']} triggered {event_type}"

    collection.insert_one(event)
    return jsonify({"status": "received"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for e in events:
        e["_id"] = str(e["_id"])
        e["timestamp"] = e["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
