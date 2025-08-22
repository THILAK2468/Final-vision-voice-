from ultralytics import YOLO #type: ignore

models = [
    YOLO("yolov8n.pt"),
    YOLO("best.pt")
]

def detect_objects(frame):
    results = []
    for model in models:
        results.extend(model(frame, conf=0.7, verbose=False))
    return results