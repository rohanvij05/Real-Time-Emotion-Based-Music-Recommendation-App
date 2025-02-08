from flask import Flask, render_template, jsonify, request
import cv2
import random
from deepface import DeepFace
import base64
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Emotion to song file mappings (each emotion has 5 songs)
emotion_tos = {
    "neutral": [
        "fix you.mp3", "kavithe song.mp3", "someone like you.mp3", 
        "tum hi ho bandhu.mp3", "senorita.mp3"
    ],
    "happy": [
        "bum bum bole.mp3", "hapier.mp3", "happy kannada.mp3", 
        "i_m yours.mp3", "ilahi.mp3"
    ],
    "angry": [
        "believer.mp3", "in the end.mp3", "mera je karda.mp3", 
        "monster.mp3", "thukra ke mera pyaar.mp3"
    ],
    "sad": [
        "kaun tujhe.mp3", "sahapati kannada.mp3", "Scientist.mp3", 
        "see you again.mp3", "tere zikr.mp3"
    ],
    "surprise": [
        "belageddu.mp3", "bye bye .mp3", "haye oye.mp3", 
        "mera wala dance.mp3", "party in usa.mp3"
    ]
}
from flask import Flask, render_template

app = Flask(__name__)

# Route for the chatbot page
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Helper function to recommend 5 songs based on emotion
def recommends(emotion):
    if emotion not in emotion_tos:
        raise ValueError(f"No songs available for the emotion: {emotion}")
    return emotion_tos[emotion]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    # Get the base64 image from frontend (webcam)
    image_data = request.json['image']
    img_data = base64.b64decode(image_data.split(',')[1])
    
    # Convert to numpy array and decode image
    np_img = np.frombuffer(img_data, dtype=np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    try:
        # DeepFace emotion detection
        analysis = DeepFace.analyze(img_path=frame, actions=['emotion'])
        dominant_emotion = analysis[0]['dominant_emotion']
        songs = recommends(dominant_emotion)
        return jsonify({"emotion": dominant_emotion, "songs": songs})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))  # Use Render's dynamic PORT or default to 5000
    app.run(host="0.0.0.0", port=port)
