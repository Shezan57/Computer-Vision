import json
import math
import cv2
import numpy as np
from ultralytics import YOLOv10
from paddleocr import PaddleOCR
import re
import os
import datetime
import sqlite3

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

cap = cv2.VideoCapture("../data/carLicence4.mp4")

# initialize the YOLOv10 model
model = YOLOv10("../weights/best.pt")

count = 0
className = ["License"]
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)

# Read the characters of the license plate
def paddle_ocr(frame, x1, y1, x2, y2):
    roi = frame[y1:y2, x1:x2]
    result = ocr.ocr(roi, det=False, rec=True, cls=False)
    text = ""
    for r in result:
        #print("ocr result:", r)
        scores = r[0][1]
        if np.isnan(scores):
            scores = 0
        else:
            scores = int(scores * 100)
        if scores > 60:
            text = r[0][0]
    pattern = re.compile('[\W]')
    text = pattern.sub('', text)
    text = text.replace("???", "")
    text = text.replace("O", "0")
    text = text.replace("粤", "1")
    return str(text)

# create a directory to save the JSON files
def save_json(lisence_plates, start_time, end_time):
    # generate individual JSON file for each 20 seconds interval
    interval_data = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "license_plates": list(lisence_plates)
    }
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    interval_file_path = f"json/output{timestamp}.json"
    with open(interval_file_path, "w") as f:
        json.dump(interval_data, f, indent=4)

    # create cumulative JSON file
    cumulative_file_path = "json/LicensePlateData.json"
    if os.path.exists(cumulative_file_path):
        with open(cumulative_file_path, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    # Add existing data to cumulative data
    existing_data.append(interval_data)

    with open(cumulative_file_path, "w") as f:
        json.dump(existing_data, f, indent=4)


# connect to the SQLite database
    save_to_database(lisence_plates, start_time, end_time)
def save_to_database(lisence_plates, start_time, end_time):
    conn = sqlite3.connect('licensePlates.db')
    cursor = conn.cursor()
    for plate in lisence_plates:
        cursor.execute(
            '''
            INSERT INTO licensePlates (start_time, end_time, License_plate)
            VALUES (?, ?, ?)
            ''',
            (start_time.isoformat(), end_time.isoformat(), plate)
        )
    conn.commit()
    conn.close()


startTime = datetime.datetime.now()
lisence_plates = set()
while True:
    ret, frame = cap.read()
    if ret:
        current_time = datetime.datetime.now()
        count += 1
        print(f"Processing frame {count}")
        results = model.predict(frame, conf=0.40)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.conf > 0.40:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame,(x1, y1),(x2, y2), (255, 0, 0), 2)
                    classNameInt = int(box.cls[0])
                    clsName = className[classNameInt]
                    conf = math.ceil(box.conf[0] * 100)/100
                    label = paddle_ocr(frame, x1, y1, x2, y2)
                    if label:
                        lisence_plates.add(label)
                    textSize = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                    c2 = x1 + textSize[0], y1 - textSize[1] - 3
                    cv2.rectangle(frame,(x1, y1), c2, (255, 0, 0), -1)
                    cv2.putText(frame, label,(x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if (current_time - startTime).total_seconds() >= 20:
            endTime = current_time
            save_json(lisence_plates, startTime, endTime)
            startTime = current_time
            lisence_plates.clear()
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()

