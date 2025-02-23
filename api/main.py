from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import websockets
from solve_tester.solve_tester import *

tasks = []
# Codes submitted by the user for each of the tasks
source_codes = []
dispatcher = None
active_task_index = 0

app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.websocket("/ws")
async def event_dispatcher(websocket: WebSocket):
    await websocket.accept()
    global dispatcher
    dispatcher = websocket
    while True:
        json_data = await websocket.receive_json()
        if json_data["event"] == "code":
            code = json_data["data"]["code"]
            index = json_data["data"]["index"]
            source_codes[index] = code

async def dispatch_event(event, data={}):
    await dispatcher.send_json({
        "event": event,
        "data": data
    })

@app.on_event("startup")
async def startup_event():
    print("Server is starting up!")
    global tasks
    global source_codes
    tasks_location = "solve_tester/tasks"
    tasks_dirs = [d for d in os.listdir(tasks_location) if os.path.isdir(os.path.join(tasks_location, d))]
    
    for d in tasks_dirs:
        if not d.isdigit() or not (0 <= int(d) < len(tasks_dirs)):
            raise Exception(f"Invalid task directory name: {d}")

    tasks = list(range(len(tasks_dirs)))
    source_codes = [""] * len(tasks)
    source_codes[0] = """#include <iostream>
    using namespace std;
    
    int main() {
        cout << "Hello, World!" << endl;
        return 0;
    }"""


@app.get("/api/cv")
async def get_cv():
    try:
        with open("cv.txt", "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        return {"error": "CV file not found."}, 404
    except Exception as e:
        return {"error": str(e)}, 500

    return {
        "message": "CV of interviewee",
        "status": "success",
        "CV": data,
    }


@app.get("/api/needs")
async def get_needs():
    try:
        with open("company_needs.txt", "r") as file:
            needs = file.readlines()
    except FileNotFoundError:
        return {"error": "company_needs.txt file not found."}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    return {
        "message": "What you should know about interviewee and what skills he should have",
        "status": "success",
        "items": needs,
    }


@app.get("/api/code")
async def get_data():
    return {
        "message": "What interviewee already coded",
        "status": "success",
        "items": source_codes[active_task_index],
    }


@app.get("/api/code_for_task")
async def get_code(index: int):
    return {
        "message": "What interviewee already coded",
        "status": "success",
        "source": source_codes[index],
    }


@app.post("/api/code_for_task")
async def upload_code(index: int, file: UploadFile = File(...)):
    try:
        source = await file.read()
        source_codes[index] = source
        return {"info": f"Code for task {index} uploaded successfully."}
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/api/tasks_statement")
async def get_task_statement(index: int):
    file_path = f"solve_tester/tasks/{index}/task_statement.md"
    if not os.path.exists(file_path):
        return {"error": 'Invalid task index.'}, 404
    try:
        with open(file_path, "r") as file:
            statement = file.readlines()
    except Exception as e:
        return {"error": str(e)}, 500
        
    await dispatch_event("start_coding", {
        "task": statement,
        "index": index
    })
    
    return {
        "message": f"Task at index {index}",
        "status": "success",
        "task": statement,
    }


@app.get("/api/tasks_hints")
async def get_task_hints_hints(index: int):
    file_path = f"solve_tester/tasks/{index}/hints.txt"
    if not os.path.exists(file_path):
        return {"error": 'Invalid task index.'}, 404
    try:
        with open(file_path, "r") as file:
            hints = file.readlines()
    except Exception as e:
        return {"error": str(e)}, 500
    return {
        "message": f"Task at index {index}",
        "status": "success",
        "task": hints,
    }


@app.get("/api/tasks_solutions")
async def get_task_solutions(index: int):
    try:
        with open(f"solve_tester/tasks/{index}/sol1.cpp", "r") as file:
            source = file.readlines()
    except FileNotFoundError:
        return {"error": "Source code file not found."}, 404
    except Exception as e:
        return {"error": str(e)}, 500

    return {
        "message": f"Task solution at index {index}",
        "status": "success",
        "source": source,
    }


@app.get("/api/tasks_results")
async def get_task_results(index: int):
    result = compile_and_test_task(source_codes[index], index, 'solve_tester/tasks')
    return result


class TextRequest(BaseModel):
    text: str

class LevelRequest(BaseModel):
    level: str

class ToxicityRequest(BaseModel):
    toxicity: int


summarized_text = ""
@app.post("/api/summarize_text")
async def post_text_summary(request: TextRequest):
    print(request.text)
    summarized_text = request.text
    return {"text": request.text} 


@app.get("/api/get_summarized_text")
async def get_summarized_text():
    return {"text": summarized_text}


@app.get("/api/run_tests")
async def post_text_summary():
    return {"text": 'tests passed'} 


summarized_english_score = ""
@app.post("/api/summarize_english_score")
async def get_sec(request: LevelRequest):
    print(request.level)
    summarized_english_score = request.level
    return {"level": request.level} 


@app.get("/api/get_summarized_english_score")
async def get_summarized_english_score():
    return {"level": summarized_english_score}


summarized_toxicity_score = ""
@app.post("/api/summarize_toxicity_score")
async def get_stc(request: ToxicityRequest):
    print(request.toxicity)
    summarized_toxicity_score = request.toxicity
    return {"toxicity": request.toxicity} 


@app.get("/api/get_summarized_toxicity_score")
async def get_summarized_toxicity_score():
    return {"toxicity": summarized_toxicity_score}


@app.get("/api/tasks_descriptions")
async def get_tasks_descriptions():
    descriptions = []
    i=0
    for index in tasks:
        file_path = f"solve_tester/tasks/{index}/description.txt"
        if not os.path.exists(file_path):
            return {"error": 'Invalid task index.'}, 404
        try:
            with open(file_path, "r") as file:
                descriptions.append(f"{i}:"+file.read())
        except Exception as e:
            return {"error": str(e)}, 500
        i+=1
    return {
        "message": f"Tasks list.",
        "status": "success",
        "task": descriptions,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)