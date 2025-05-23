from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class QuizRequest(BaseModel):
    topic: str
    level: str

@app.post("/generate-quiz")
async def generate_quiz(req: QuizRequest):
    try:
        prompt = f"Create 5 multiple choice English quiz questions for {req.level} level on the topic: {req.topic}. Format the response as numbered questions with 4 options and mark the correct answer."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return {"quiz": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to AI Language Coach API"}