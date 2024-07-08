from ultralytics import YOLO
import cv2
import numpy as np
import time
import torch
import os

# Check if CUDA is available and set the device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Define the model name
model_name = "yolov8n.pt"

# Check if the model file exists, if not, download it
if not os.path.exists(model_name):
    print(f"Downloading {model_name}...")
    YOLO(model_name)  # This will download the model
    print("Download complete.")

# Load the YOLOv8 model
model = YOLO(model_name)
model.to(device)  # Move model to GPU if available

# Open the USB camera (usually 0 for the default camera)
cap = cv2.VideoCapture(0)

# Set a smaller frame size for faster processing
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variables for FPS calculation
prev_time = 0
fps = 0

# Warm up the model
dummy_input = torch.randn(1, 3, 480, 640).to(device)
model(dummy_input)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Get the current time for FPS calculation
    current_time = time.time()
    
    # Calculate FPS
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Preprocess the frame
    input_frame = cv2.resize(frame, (640, 480))
    input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
    input_frame = input_frame.transpose((2, 0, 1))
    input_frame = np.ascontiguousarray(input_frame)
    input_frame = torch.from_numpy(input_frame).to(device)
    input_frame = input_frame.float() / 255.0
    input_frame = input_frame.unsqueeze(0)

    # Run inference on the frame
    with torch.no_grad():
        results = model(input_frame)

    # Process results and draw bounding boxes
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        
        for box, cls, conf in zip(boxes, classes, confidences):
            if conf > 0.5:  # Confidence threshold
                x1, y1, x2, y2 = map(int, box)
                class_name = result.names[int(cls)]
                
                # Draw rectangle and put class name
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display FPS on the frame
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with detections and FPS
    cv2.imshow("Real-time Object Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
