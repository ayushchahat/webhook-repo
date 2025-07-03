# 🔔 Webhook Dashboard – GitHub Webhook Receiver

This is a **Flask-based webhook receiver** that listens for GitHub events like **pushes** and **pull requests**, stores them in **MongoDB Atlas**, and displays them via a responsive frontend.  
The project is deployed live using **Render** and supports GitHub integration via webhooks.

---

## 🌐 Live Demo

**Frontend UI**  
➡️ [https://webhook-repo-29uf.onrender.com](https://webhook-repo-29uf.onrender.com)

**JSON API Endpoint**  
➡️ [https://webhook-repo-29uf.onrender.com/events](https://webhook-repo-29uf.onrender.com/events)

---

## 📌 Features

- ✅ Receives GitHub webhook events (`push`, `pull_request`)
- ✅ Stores event logs in **MongoDB Atlas**
- ✅ `/events` API endpoint to retrieve events in JSON
- ✅ Frontend dashboard that auto-refreshes every 15 seconds
- ✅ Deployed on **Render** (Free Tier)
- ✅ Works with **ngrok** for local development

---

## ⚙️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Database**: MongoDB Atlas
- **Deployment**: Render
- **Webhook Tunnel (local only)**: ngrok

---

## 🚀 Setup Instructions (Local)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/ayushchahat/webhook-repo.git
cd webhook-repo
---

## 🛠️ Local Setup

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate   # On macOS/Linux
webhook-repo/
├── app.py                # Flask application logic
├── requirements.txt      # Dependencies for deployment
├── Procfile              # For Render deployment
├── templates/
│   └── index.html        # Frontend UI
└── render.yaml (optional)
---

## ✍️ Author

**Ayush Chahat**  
📧 [ayush110903kumar@gmail.com](mailto:ayush110903kumar@gmail.com)  
🔗 [https://github.com/ayushchahat](https://github.com/ayushchahat)
