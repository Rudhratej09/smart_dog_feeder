from ultralytics import YOLO
import serial
import cv2
import time

COM_PORT = "COM3"
BAUD_RATE = 9600
ser = None


try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  
    print(f" Serial communication established on {COM_PORT}")
except Exception as e:
    print(f" Error initializing serial: {e}")


model = YOLO("yolov8n.pt")


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(" Error: Unable to open camera")
    exit()

dog_detected = False  
cooldown_time = 30 
last_trigger_time = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print(" No frame received. Exiting loop.")
        break


    results = model(frame)
    detected_now = False

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])  
            label = model.names[class_id]  

            if label == "dog":
                detected_now = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    current_time = time.time()
    if detected_now and not dog_detected and (current_time - last_trigger_time > cooldown_time):
        dog_detected = True
        last_trigger_time = current_time
        if ser:
            ser.write(b"DOG_DETECTED\n")
            print(" Dog detected! Sent command to ESP32.")

    
    if dog_detected and (current_time - last_trigger_time > cooldown_time):
        dog_detected = False

    cv2.imshow("YOLOv8 Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()
    print(" Serial connection closed.")