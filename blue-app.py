# blue-app.py
import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

TEAM_COLOR = os.environ.get("TEAM_COLOR", "blue")
TEAM_NAME  = os.environ.get("TEAM_NAME",  "Blue Team")
BG_COLOR   = os.environ.get("BG_HEX",     "#1a237e")
ACCENT     = os.environ.get("ACCENT_HEX", "#42a5f5")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoteVibe — {{ team_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: {{ bg_color }};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .card {
            background: rgba(255,255,255,0.08);
            border: 2px solid {{ accent }};
            border-radius: 24px;
            padding: 60px 80px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }
        h1 { font-size: 3.5rem; font-weight: 800; margin-bottom: 8px; }
        .tagline { font-size: 1.2rem; opacity: 0.7; margin-bottom: 40px; }
        .vote-count {
            font-size: 5rem;
            font-weight: 900;
            color: {{ accent }};
            margin: 20px 0;
        }
        .vote-btn {
            background: {{ accent }};
            color: #000;
            border: none;
            padding: 18px 60px;
            font-size: 1.4rem;
            font-weight: 700;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .vote-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .footer {
            margin-top: 30px;
            font-size: 0.85rem;
            opacity: 0.5;
        }
        .pod-info {
            margin-top: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 0.8rem;
            font-family: monospace;
            opacity: 0.6;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔵 {{ team_name }}</h1>
        <p class="tagline">CloudVibe Internal Voting System</p>
        <div class="vote-count">{{ vote_count }}</div>
        <p style="margin-bottom: 20px; opacity: 0.7;">votes cast</p>
        <form method="POST" action="/vote">
            <button class="vote-btn" type="submit">Cast Your Vote</button>
        </form>
        <div class="pod-info">
            Pod: {{ pod_name }} | Namespace: {{ namespace }}
        </div>
        <p class="footer">VoteVibe v1.0 · CloudVibe Tech Internal Tools</p>
    </div>
</body>
</html>
"""

votes = 0

@app.route("/")
def index():
    return render_template_string(
        TEMPLATE,
        team_name=TEAM_NAME,
        bg_color=BG_COLOR,
        accent=ACCENT,
        vote_count=votes,
        pod_name=os.environ.get("HOSTNAME", "unknown"),
        namespace=os.environ.get("POD_NAMESPACE", "unknown")
    )

@app.route("/vote", methods=["POST"])
def vote():
    global votes
    votes += 1
    return redirect(url_for("index"))

@app.route("/healthz")
def health():
    return {"status": "ok", "team": TEAM_NAME}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
