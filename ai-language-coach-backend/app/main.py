# Have to make some things again. Don't forget, connect it to frontend.
# For now, quiz generator and  I want to make an essay feedback generator.
# Now, quiz generator gives multiple choice questions with 4 options.
# Will add more quiz types.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# need this to validate the request body(!important!don't delete)
import openai
import os
from dotenv import load_dotenv

# this reads my keys(!important!don't delete)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


# I want the quiz topic and the level from user
class QuizRequest(BaseModel):
    topic: str
    level: str


@app.post("/generate-quiz")
async def generate_quiz(req: QuizRequest):
    try:
        prompt = f"""Create 5 multiple choice English quiz questions for
        {req.level} level on the topic: {req.topic}. Format the response
        as numbered questions with 4 options.""".strip()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return {"quiz": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# temperature=0.0 is more deterministic, 2.0 is more creative.
# goes from 0.0 to 2.0, general default recommended that I found is 0.7.


@app.get("/")
async def root():
    return {"message": "Welcome to AI Language Coach API"}
