import cv2
import matplotlib.pyplot as plt
import pygame
import time
from pothole_detector import detect_potholes  # Import the detection function

# Initialize pygame for audio alerts
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("buzz.mp3")  # Ensure the file exists

# Define function to display images
def plt_show(image, title=""):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.axis("off")
    plt.title(title)
    plt.imshow(image, cmap="gray" if len(image.shape) == 2 else None)
    plt.show()

# Load a test image
image_path = "Pothole.jpg"  # Ensure the image exists
image = cv2.imread(image_path)

# Define detection parameters
threshold_value = 12
min_area = 2800
sensitivity = 0.6

# Process the image
processed_image, potholes = detect_potholes(image, threshold_value, min_area, sensitivity)

# Show the output
plt_show(processed_image, title="Detected Potholes")

# Play alert sound after detection (if potholes found)
if potholes:
    pygame.mixer.music.play()
    time.sleep(3)  # Play for 3 seconds
    pygame.mixer.music.stop()
