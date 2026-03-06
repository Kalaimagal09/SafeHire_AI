from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib

app = FastAPI()

# 1. ENABLE CORS (Crucial for the Chrome Extension to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. LOAD YOUR TRAINED AI MODEL
try:
    model = joblib.load('safehire_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print("❌ Error loading model. Did you run train_model.py?")

# 3. DEFINE THE DATA STRUCTURE
class QuestionRequest(BaseModel):
    text: str

# Helper function to give the UI specific legal details based on HR laws
def get_violation_details(text: str):
    text = text.lower()
    if any(word in text for word in ["age", "birth", "retire", "old", "young"]):
        return "Age Discrimination", "If hired, can you furnish proof of age?"
    elif any(word in text for word in ["married", "kids", "children", "child", "pregnant", "maiden", "mrs", "miss"]):
        return "Marital/Family Status", "Can you meet the specified work schedule?"
    elif any(word in text for word in ["citizen", "country", "born", "language", "nationality"]):
        return "National Origin/Citizenship", "Do you have the legal right to work in the U.S.?"
    elif any(word in text for word in ["handicap", "disability", "medical", "health"]):
        return "Disability/Health", "How would you perform this particular task?"
    elif any(word in text for word in ["religion", "church", "pastor"]):
        return "Religion/Creed", "Can you work the required days and shifts?"
    else:
        return "General Compliance Violation", "Please focus questions strictly on job-related duties."

# 4. THE PREDICTION ENDPOINT
@app.post("/predict")
async def predict_question(request: QuestionRequest):
    # Convert text to numbers using the loaded vectorizer
    X_input = vectorizer.transform([request.text])
    
    # Predict using the Logistic Regression model (1 = Illegal, 0 = Safe)
    prediction = model.predict(X_input)[0]
    
    if prediction == 1:
        category, alternative = get_violation_details(request.text)
        return {
            "is_flagged": True,
            "category": category,
            "risk_score": 95,
            "safe_alternative": alternative
        }
    else:
        return {
            "is_flagged": False,
            "category": "None",
            "risk_score": 5,
            "safe_alternative": "N/A"
        }