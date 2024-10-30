from config.dependencies import get_hands, get_vjoy_device
from services.hand_service import update_vjoy_hand_gestures

def process_hand_landmarks(frame_rgb):
    hands = get_hands()
    vjoy_device = get_vjoy_device()
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            update_vjoy_hand_gestures(hand_landmarks, vjoy_device)
