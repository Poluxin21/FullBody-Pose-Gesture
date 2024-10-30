import numpy as np

def calculate_head_movement(landmarks, frame_width, frame_height):
    left_eye = np.array([(landmarks[362].x * frame_width, landmarks[362].y * frame_height)])
    right_eye = np.array([(landmarks[33].x * frame_width, landmarks[33].y * frame_height)])

    eye_center = (left_eye + right_eye) / 2

    gaze_direction = "Center"
    if eye_center[0, 0] < frame_width * 0.3:
        gaze_direction = "Left"
    elif eye_center[0, 0] > frame_width * 0.7:
        gaze_direction = "Right"

    return gaze_direction
