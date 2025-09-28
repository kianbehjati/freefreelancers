from fastapi import FastAPI
from google import genai
import dotenv

app = FastAPI()
dotenv.load_dotenv()
client = genai.Client()


@app.get('/')
def root():
    genai_response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents="Hello, world!"
    )
    return {"message": genai_response.text}

