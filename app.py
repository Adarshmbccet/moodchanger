
from flask import Flask, render_template
import cv2
from fer import FER
import pywhatkit
import threading
import random

app = Flask(__name__)

mood_to_music = {
    "happy": ["sad songs ", "lonely piano", "heartbreak songs"],
    "sad": ["crazy edm", "funny songs", "party bollywood"],
    "angry": ["calm meditation music", "soothing flute"],
    "fear": ["motivational songs", "courage bollywood"],
    "disgust": ["comedy scenes", "funny animal videos"],
    "surprise": ["chill lo-fi", "soft melodies"],
    "neutral": ["emotional piano", "nostalgic music"]
}

def detect_mood():
    detector = FER(mtcnn=False)
    cap = cv2.VideoCapture(0)
    for _ in range(5):  # Warm-up
        cap.read()
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "neutral"

    mood = detector.top_emotion(frame)
    if mood:
        return mood[0]
    return "neutral"

def play_opposite_music(mood):
    song_list = mood_to_music.get(mood, ["sad songs"])
    song = random.choice(song_list)
    print(f"Detected mood: {mood}. Playing: {song}")
    pywhatkit.playonyt(song)

@app.route('/')
def home():
    mood = detect_mood()
    threading.Thread(target=play_opposite_music, args=(mood,), daemon=True).start()
    return render_template("index.html", mood=mood)

if __name__ == "__main__":
 print("Visit the assistant at: http://127.0.0.1:5000") 
app.run(debug=True,port=5000)


