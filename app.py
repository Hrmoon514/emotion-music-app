# app.py (このコードを貼り付けてください)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Flaskアプリを初期化
app = Flask(__name__)
CORS(app)

# Beatoven.ai APIの設定
BEATOVEN_API_URL = "https://api.beatoven.ai/v1/tracks"
BEATOVEN_API_KEY = "YOUR_API_KEY" # ここを実際のAPIキーに書き換えてください

# 感情と音楽スタイルのマッピング
EMOTION_TO_MUSIC_PROMPT = {
    "happy": "upbeat, happy, pop, synthesizer",
    "sad": "sad, melancholic, piano solo, slow tempo",
    "excited": "energetic, exciting, rock, fast tempo, drums",
    "calm": "calm, peaceful, ambient, strings"
}

@app.route('/generate-music', methods=['POST'])
def generate_music():
    data = request.get_json()
    emotion = data.get('emotion')

    if not emotion:
        return jsonify({"error": "Emotion not provided"}), 400

    prompt = EMOTION_TO_MUSIC_PROMPT.get(emotion, "neutral, background music")
    print(f"受け取った感情: {emotion}, 生成する音楽の指示: {prompt}")

    headers = {
        "X-API-KEY": BEATOVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "title": f"{emotion} music",
        "prompts": [prompt]
    }
    
    try:
        response = requests.post(BEATOVEN_API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        
        track_data = response.json()
        print(f"APIからの応答: {track_data}")
        
        music_url = track_data.get("url", "https://www.beatoven.ai/track/some-id") 

        return jsonify({"message": "Music generation started!", "musicUrl": music_url})

    except requests.exceptions.RequestException as e:
        print(f"APIエラー: {e}")
        return jsonify({"error": "Failed to call music API"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
