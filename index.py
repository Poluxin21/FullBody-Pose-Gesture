import cv2
import mediapipe as mp
import pyvjoy 

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

vjoy_device = pyvjoy.VJoyDevice(1)

def update_vjoy(hand_landmarks):
    # Mapear posição do indicador (ponto 8) e dedão (ponto 4)
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    
    # Calcular distância entre dedão e indicador para definir um 'pinch' (gesto de agarrar)
    distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
    
    if distance < 0.1:
        vjoy_device.set_button(1, 1)
        print("Fechando a Mão")
    else:
        vjoy_device.set_button(1, 0) 
        print("Abrindo a mão")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            update_vjoy(hand_landmarks) 
    
    cv2.imshow("Detecção de Mãos", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
