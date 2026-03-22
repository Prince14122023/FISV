from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
import cv2
import numpy as np
import base64
import os
import sys


sys.path.append(os.path.dirname(__file__))
try:
    from detector import analyze_fabric 
except ImportError:
    from .detector import analyze_fabric

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Online", "message": "FIS PRO Backend Engine is Running Successfully"}

@app.post("/api/analyze-frame")
async def analyze_frame(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return JSONResponse(content={"error": "Invalid image format"}, status_code=400)

        
        processed_frame, status, defect, brief, acc = analyze_fabric(frame)

        
        _, buffer = cv2.imencode('.jpg', processed_frame)
        b64_str = base64.b64encode(buffer).decode('utf-8')

        return {
            "image": f"data:image/jpeg;base64,{b64_str}",
            "status": status,
            "defect_type": defect,
            "briefing": brief,
            "accuracy": acc
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


app = app