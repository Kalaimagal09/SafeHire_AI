import speech_recognition as sr
import requests

# Make sure this matches your FastAPI URL!
API_URL = "http://127.0.0.1:8000/predict" 

def run_live_audit():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n" + "="*50)
        print("🎤 Adjusting for background noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=2)
        print("🔴 LIVE: You are the HR Manager. Ask a question now!")
        
        try:
            # Listen to the microphone
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("🔄 Transcribing speech to text...")
            
            # Convert audio to text using Google's free speech-to-text
            spoken_text = r.recognize_google(audio)
            print(f"\n🗣️ You said: '{spoken_text}'")
            
            # Send the text to your FastAPI Backend
            print("🚀 Sending to SafeHire AI Backend...")
            response = requests.post(API_URL, json={"text": spoken_text})
            
            if response.status_code == 200:
                result = response.json()
                print("-" * 30)
                if result.get("is_flagged"):
                    print(f"🚨 ILLEGAL QUESTION DETECTED!")
                    print(f"📌 Violation: {result.get('category')}")
                    print(f"💡 Safe Alternative: {result.get('safe_alternative')}")
                else:
                    print("✅ SAFE QUESTION! Good job.")
                print("="*50 + "\n")
            else:
                print("❌ Backend Error: Make sure your FastAPI server is running!")
                
        except sr.UnknownValueError:
            print("🤷 Could not understand the audio. Please try again.")
        except sr.RequestError:
            print("🔌 Internet error. Speech recognition needs a connection.")

if __name__ == "__main__":
    while True:
        run_live_audit()
        # Press Ctrl+C in the terminal to stop the loop