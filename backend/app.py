import os
import time
from typing import Optional

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "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"
_default_model = "openai/gpt-oss-20b"
GROQ_MODEL = os.getenv("GROQ_MODEL", _default_model)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
COMPLETENESS_HINT = "Répond en message complet, termine tes phrases, ne coupe pas la sortie. Met pleins d'emojis dans tes messages."

AGENTS = {
    "amogus": {
        "prompt": "Tu es un personnage Among Us. Tu es très sus. Tu es un imposteur mais tu dois le cacher. Répond à chaque requête avec une réponse suspecte, des références, du brainrot, du sigma, et surtout du SUS",
        "model": None,
    },
    "banane": {
        "prompt": "Tu es une banane. Tu fais des blagues sur les bananes à chaque réponse.",
        "model": None,
    },
    "pikachu": {
        "prompt": "Remplace tous les motrs par Pika Pika. ",
        "model": None,
    },
}


def call_groq(user_message: str, prompt: str, agent: str) -> str:
    agent_key = agent.lower().strip() if agent else "amogus"
    agent_conf = AGENTS.get(agent_key) or AGENTS["amogus"]
    base_prompt = prompt.strip() if prompt else agent_conf["prompt"]
    system_prompt = f"{base_prompt}\n{COMPLETENESS_HINT}"
    model = agent_conf.get("model") or GROQ_MODEL

    def _fallback_reply(kind: str) -> str:
        if kind == "pikachu":
            return "Pika pika !" if not user_message else f"Pika pika : {user_message}"
        if kind == "banane":
            return "La banane rebondit : " + (user_message or "reformule")
        return "Sus detected : " + (user_message or "parle encore")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.5,
        "max_tokens": 1024,
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    attempts = 0

    while attempts < 3:
        attempts = 0
        try:
            resp = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
            if resp.status_code != 200:
                time.sleep(0.25)
                continue

            data = resp.json()
            choices = data.get("choices") or []
            if not choices:
                time.sleep(0.2)
                continue

            def _pick_content() -> Optional[str]:
                for choice in choices:
                    message_obj = choice.get("message") or {}
                    if not isinstance(message_obj, dict):
                        continue
                    for key in ("content", "text", "message"):
                        value = message_obj.get(key)
                        if isinstance(value, str) and value.strip():
                            return value.strip()
                        if isinstance(value, list):
                            collected: list[str] = []
                            for part in value:
                                if isinstance(part, dict):
                                    txt = part.get("text") or part.get("content")
                                    if isinstance(txt, str) and txt.strip():
                                        collected.append(txt.strip())
                            if collected:
                                return " ".join(collected).strip()
                return None

            content = _pick_content()
            if content:
                return content

            time.sleep(0.2)
        except Exception as exc:
            time.sleep(0.4)

    base = _fallback_reply(agent_key)
    return base


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    prompt = str(payload.get("prompt", "")).strip()
    agent = str(payload.get("agent", "amogus"))
    if not message:
        return jsonify({"error": "message manquant"}), 400

    reply = call_groq(message, prompt, agent)
    return jsonify({"reply": reply, "provider": "groq", "agent": agent, "timestamp": int(time.time())})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "up", "provider": "groq", "hasKey": bool(GROQ_API_KEY)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
