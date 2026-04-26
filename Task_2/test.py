from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from ultralytics import YOLO

app = FastAPI(title="Drone Detection API")

model = YOLO("yolov8n.pt")

DRONE_CLASSES = ["bird", "airplane", "kite"]

@app.get("/")
def home():
    return {"message": "Drone Detection API is running"}

@app.post("/detect")
async def detect_drones(file: UploadFile = File(...)):
    
    image_bytes = await file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(img)

    detections = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])

            if label in DRONE_CLASSES and conf > 0.5:
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "label": "drone"   
                })

    return {
        "total_drones": len(detections),
        "detections": detections
    }