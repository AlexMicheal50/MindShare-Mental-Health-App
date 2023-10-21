from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from time import sleep
import main
app = FastAPI()

templates = Jinja2Templates(directory="templates")
class TranscriptionData(BaseModel):
    transcription: str

previous_questions_and_answers = []
@app.get("/")
def chat():
    print ("hello")

@app.get("/chat/", response_class=HTMLResponse)
async def render_template(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_transcription")
async def process_transcription(data: TranscriptionData):    
    try:
         # Your processing logic here
        sleep(2)
        transcribed_text = data.transcription
        new_question = f"In ten lines or less, answer: {transcribed_text}"
        # print(f"transcribed text {transcribed_text}")
        errors = main.get_moderation(new_question)
        if errors:
            raise f"You did not pass the moderation check"
        response = main.get_response(main.INSTRUCTIONS, previous_questions_and_answers, new_question)
        previous_questions_and_answers.append((new_question, response))
        print(f"Response: {response}")
        return {"message": f"{response}"}
    except Exception as e:
        return{"message": f"Error: {e}"}

if __name__ == "__main__":
    uvicorn.run("views:app", host="0.0.0.0", port=8000, reload=True)
