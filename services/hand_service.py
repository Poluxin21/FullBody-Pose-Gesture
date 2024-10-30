import mediapipe as mp

def update_vjoy_hand_gestures(hand_landmarks, vjoy_device):
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    
    distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
    
    if distance < 0.1:
        vjoy_device.set_button(1, 1)
    else:
        vjoy_device.set_button(1, 0)
