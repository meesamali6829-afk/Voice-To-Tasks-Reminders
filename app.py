import os
from groq import Groq
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from gtts import gTTS 
import subprocess

# 1. Groq Setup
client = Groq(api_key="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")

app = Flask(__name__)
CORS(app)

# Voice function (Mobile compatible)
def speak_mobile(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("response.mp3")
        # Android par file play karne ke liye (Pydroid support)
        os.system("termux-media-player play response.mp3" if os.name != 'nt' else "start response.mp3")
    except:
        print("Voice play nahi ho saki")

# --- UI ROUTE ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_command():
    data = request.json
    user_query = data.get('query', '').lower()
    
    response_text = ""
    
    # --- ALL-OF-ALL SYSTEM HANDLER ---
    
    # Mobile/PC Apps Control
    if "open notepad" in user_query or "open editor" in user_query:
        # Agar PC par hain to notepad, mobile par hain to message
        response_text = "System command process ho rahi hai."
        try:
            if os.name == 'nt': subprocess.Popen(['notepad.exe'])
        except: pass
        
    elif "open calculator" in user_query:
        response_text = "Calculator khol raha hoon."
        try:
            if os.name == 'nt': subprocess.Popen(['calc.exe'])
        except: pass

    # --- GROQ BRAIN (Super Fast) ---
    else:
        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192", 
                messages=[
                    {"role": "system", "content": "You are Aura AI. Respond in short, clear sentences in Hindi/Urdu. You handle all system tasks."},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            response_text = completion.choices[0].message.content
        except Exception as e:
            response_text = "Groq connection error."

    # Bolne ka kaam (Optional: Browser se karwana behtar hai mobile par)
    # speak_mobile(response_text) 

    return jsonify({"response": response_text})

if __name__ == '__main__':
    # Mobile par run karne ke liye 0.0.0.0 zaroori ho sakta hai
    app.run(host='0.0.0.0', port=5000, debug=True)
