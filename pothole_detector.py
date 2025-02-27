import cv2
import numpy as np
import pygame
import time

def detect_potholes(frame, threshold_value=150, min_area=1000, sensitivity=0.5):
    """
    Detects potholes in a given frame using contour detection.
    
    Args:
        frame (numpy array): Input image (frame) from video.
        threshold_value (int): Threshold value for binarization.
        min_area (int): Minimum area to consider a pothole.
        sensitivity (float): Sensitivity for detection.

    Returns:
        processed_frame (numpy array): Frame with detected potholes marked.
        potholes (list): List of detected potholes with bounding box info.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply threshold
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    potholes = []
    processed_frame = frame.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue  # Ignore small contours

        # Get bounding box
        x, y, w, h = cv2.boundingRect(c)

        # Store detected pothole
        potholes.append({"x": x, "y": y, "w": w, "h": h, "area": area})

        # Draw rectangle and label
        cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(processed_frame, 'Pothole', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 255, 0), 2)

    return processed_frame, potholes

def play_alert_sound():
    """
    Plays an alert sound when a pothole is detected.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("buzz.mp3")
    pygame.mixer.music.play()
    time.sleep(5)  # Play for 2 seconds
    pygame.mixer.music.stop()
