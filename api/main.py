from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

tasks = [1,2,3]

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/api/cv")
async def get_cv():
    data = open("cv.txt", "r").readlines()
    print(data)
    return {
        "message": "CV of interviewee",
        "status": "success",
        "CV": data,
    }
@app.get("/api/needs")
async def get_needs():
    return {
        "message": "What you should know about interviewee and what skills he should has",
        "status": "success",
        "items": ["assembly"],
    }
@app.get("/api/code")
async def get_code():
    data = open("code.txt", "r").readlines()
    return {
        "message": "What interviewee already coded",
        "status": "success",
        "code": data,
    }
@app.get("/api/tasks_statement")
async def get_task_statment(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": ['say dog', 'write binsearch', 'say hubert'][index],
        }
    return {"error": 'handle this smh'}, 404

@app.get("/api/tasks_hints")
async def get_task_hints(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": ['say dog', 'divide evertyhing in two parts', 'say hubert'][index],
        }
    return {"error": 'handle this smh'}
@app.get("/api/tasks_solutions")
async def get_task_solutions(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": [['dog'], ['its simple'], ['hubert']][index],
        }
    return {"error": 'handle this smh'}

@app.get("/api/tasks_results")
async def get_task_results(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": ['task went great','task went great','task went great'][index],
        }
    return {"error": 'handle this smh'}

class TextRequest(BaseModel):
    text: str
class LevelRequest(BaseModel):
    level: str
class ToxicityRequest(BaseModel):
    toxicity: int
@app.post("/api/summarize_text")
async def post_text_summary(request: TextRequest):
    print(request.text)
    return {"text": request.text} 
@app.get("/api/run_tests")
async def post_text_summary():
    return {"text": 'tests passed'} 
@app.post("/api/summarize_english_score")
async def get_sec(request: LevelRequest):
    print(request.level)
    return {"level": request.level} 

@app.post("/api/summarize_toxicity_score")
async def get_stc(request: ToxicityRequest):
    print(request.toxicity)
    return {"toxicity": request.toxicity} 

@app.get("/api/tasks_descriptions")
async def get_task_descriptions():
    return {
        "message": f"Summar of interview code score",
        "status": "success",
        "task": ['0. c++ task', '1. assembly task', '2. java task'],
    }
if __name__ == "__main__":
    print("Uruchamiam serwer!")
    uvicorn.run(app, host="127.0.0.1", port=8080)
