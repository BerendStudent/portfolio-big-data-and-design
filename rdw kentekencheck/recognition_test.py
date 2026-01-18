from ultralytics import YOLO
import cv2
from utils import preprocess_plate, read_plate

model = YOLO("rdw kentekencheck/model/yolov8n.pt")

img = cv2.imread("rdw kentekencheck/images/test.jpg")
results = model(img, conf=0.3)

for box in results[0].boxes.xyxy:
    x1, y1, x2, y2 = map(int, box)
    plate = img[y1:y2, x1:x2]

    processed = preprocess_plate(plate)
    text = read_plate(processed)

    print("Detected plate:", text)

    cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
    cv2.putText(img, text, (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

cv2.imshow("Result", img)
cv2.waitKey(0)
