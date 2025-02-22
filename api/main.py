from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
async def get_data():
    data = open("cv.txt", "r").readlines()
    print(data)
    return {
        "message": "CV of interviewee",
        "status": "success",
        "items": data,
    }
@app.get("/api/needs")
async def get_data():
    return {
        "message": "What you should know about interviewee and what skills he should has",
        "status": "success",
        "items": ["Algorithmic thinking", "Python", "Django", "FastAPI"],
    }
@app.get("/api/code")
async def get_data():
    return {
        "message": "What interviewee already coded",
        "status": "success",
        "items": "list.bin_search(3)",
    }
@app.get("/api/tasks_statement/{index}")
async def get_task(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": ['say dog', 'say monkey', 'say hubert'][index],
        }
    return {"error": 'handle this smh'}, 404

@app.get("/api/tasks_hints/{index}")
async def get_task(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": ['say dog', 'say monkey', 'say hubert'][index],
        }
    return {"error": 'handle this smh'}
@app.get("/api/tasks_solutions/{index}")
async def get_task(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": [['dog'], ['monkey'], ['hubert']][index],
        }
    return {"error": 'handle this smh'}

@app.get("/api/tasks_results/{index}")
async def get_task(index: int):
    if 0 <= index < len(tasks):
        return {
            "message": f"Task at index {index}",
            "status": "success",
            "task": ['task went great'][index],
        }
    return {"error": 'handle this smh'}

@app.get("/api/summarize_text")
async def get_task():
    return {
        "message": f"Summar of interview",
        "status": "success",
        "task": "text",
    }
    
@app.get("/api/summarize_english_score")
async def get_task():
    return {
        "message": f"Summar of interview english fluency",
        "status": "success",
        "task": "english score",
    }

@app.get("/api/summarize_toxicity_score")
async def get_task():
    return {
        "message": f"Summar of interview toxicity",
        "status": "success",
        "task": "toxicity score",
    }
@app.get("/api/tasks_descriptions")
async def get_task():
    return {
        "message": f"Summar of interview code score",
        "status": "success",
        "task": ['c++ task', 'python task', 'java task'],
    }
if __name__ == "__main__":
    print("Uruchamiam serwer!")
    uvicorn.run(app, host="127.0.0.1", port=8080)
