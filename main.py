from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Project Aura Prediction API")

@app.get("/")
def home():
    return {"status": "Online", "location": "Juja, Kenya", "system": "Raspberry Pi 5"}

@app.get("/predict/nutrients")
def predict_nutrients(months_old: int):
    # Logic based on your Avocado Roadmap
    if months_old < 6:
        return {"action": "Apply 150g NPK", "urgency": "High"}
    elif 6 <= months_old < 12:
        return {"action": "Apply 250g CAN", "urgency": "Medium"}
    return {"action": "Check Manual for Mature Trees", "urgency": "Low"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add your Blogger domain here
origins = [
    "https://powerdreams.top",
    "https://www.powerdreams.top",
    "https://yourblogname.blogspot.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live-status")
def get_status():
    return {
        "temp": 24.5, 
        "moisture": "42%", 
        "last_fertilized": "March 10"
    }
