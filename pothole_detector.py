from ultralytics import YOLO
import cv2
import numpy as np
import pygame
import time

# Load a more accurate YOLOv8 model for pothole detection
model = YOLO("yolov8m.pt")  # Change to 'yolov8m' or a fine-tuned pothole detection model if available

def detect_potholes(frame, conf_threshold=0.5):
    """
    Detects potholes in a given frame using YOLOv8.

    Args:
        frame (numpy array): Input image (frame) from video.
        conf_threshold (float): Confidence threshold for detections.

    Returns:
        processed_frame (numpy array): Frame with detected potholes marked.
        potholes (list): List of detected potholes with bounding box info.
    """
    results = model(frame)[0]  # Run YOLOv8 on the frame
    potholes = []
    processed_frame = frame.copy()

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])

        if confidence >= conf_threshold:
            potholes.append({"x": x1, "y": y1, "w": x2 - x1, "h": y2 - y1, "confidence": confidence})
            
            # Draw bounding box and label with better visualization
            color = (0, 255, 0) if confidence > 0.7 else (0, 255, 255)
            cv2.rectangle(processed_frame, (x1, y1), (x2, y2), color, 3)
            label = f'Pothole ({confidence:.2f})'
            cv2.putText(processed_frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return processed_frame, potholes

def play_alert_sound():
    """
    Plays an alert sound when a pothole is detected.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("buzz.mp3")
    pygame.mixer.music.play()
    time.sleep(2)
    pygame.mixer.music.stop()
