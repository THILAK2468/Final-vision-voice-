import cv2 #type: ignore
import time
import settings as config
from vision import detect_objects
from audio import speak_text
from ocr import extract_text
from utils import (
    get_direction, update_counter, is_approaching,
    object_counter, prev_boxes, priority_classes
)
from translate import translate_label

last_announced = {}
last_text = ""

cap = cv2.VideoCapture(0)
fps_start = time.time()
frame_count = 0

langs = list(config.available_languages.keys())

print(f"Language: {config.available_languages[config.user_language]}")
print(f"OCR Enabled: {config.ocr_enabled} (Press 't' to toggle OCR, 'l' to change language)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    announce_made = False
    combined_results = detect_objects(frame)

    for r in combined_results:
        boxes = r.boxes.xyxy.cpu().numpy()
        cls = r.boxes.cls.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()

        for box, c, conf in zip(boxes, cls, confs):
            label = r.names[int(c)] if hasattr(r, 'names') else "object"
            translated_label = translate_label(label)
            x1, y1, x2, y2 = map(int, box)
            cx = (x1 + x2) // 2
            direction = get_direction(cx, frame.shape[1])
            distance = x2 - x1
            announce_key = f"{label}_{direction}"

            count = update_counter(label, direction)
            prev_box = prev_boxes.get(label)

            if label in priority_classes and is_approaching(box, prev_box):
                text_out = f"{translated_label} {direction} నుండి వస్తోంది"
                print("Priority Alert:", text_out)
                speak_text(text_out)
                last_announced[announce_key] = distance
                announce_made = True
            elif count >= 3 and (
                announce_key not in last_announced or distance > last_announced[announce_key] + 50):
                text_out = f"{translated_label} {direction} లో ఉంది"
                print("Announcing Object:", text_out)
                speak_text(text_out)
                last_announced[announce_key] = distance
                announce_made = True

            prev_boxes[label] = box

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.arrowedLine(frame, (cx, y2), (cx, y2 + 20), (255, 0, 0), 2)

    if not announce_made and config.ocr_enabled:
        text = extract_text(frame)
        if text and text != last_text:
            print("OCR Text:", text)
            speak_text(text)
            last_text = text

    frame_count += 1
    if frame_count >= 10:
        fps = int(10 / (time.time() - fps_start))
        fps_start = time.time()
        frame_count = 0
        cv2.putText(frame, f"FPS: {fps}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.putText(frame, f"Lang: {config.available_languages[config.user_language]}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("VisionVoice", frame)
    

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('t'):
        config.ocr_enabled = not config.ocr_enabled
        print(" OCR Toggled:", config.ocr_enabled)
    elif key == ord('l'):
        current_index = langs.index(config.user_language)
        next_index = (current_index + 1) % len(langs)
        config.user_language = langs[next_index]
        print(f" Language switched to: {config.available_languages[config.user_language]}")

cap.release()
cv2.destroyAllWindows()