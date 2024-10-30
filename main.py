import cv2
from config.freePIE_init import init_freePie
from utils.video_utils import start_video_capture, release_video_capture
from controllers.hand_controller import process_hand_landmarks
from controllers.head_controller import process_head_landmarks

init_freePie("path/to/freepie")

cap = start_video_capture()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_height, frame_width, _ = frame.shape
    
    # Processar mãos
    process_hand_landmarks(frame_rgb)
    
    # Processar cabeça e direção de olhar
    gaze_direction = process_head_landmarks(frame_rgb, frame_width, frame_height)
    if gaze_direction:
        cv2.putText(frame, f"Direção do Olhar: {gaze_direction}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    cv2.imshow("Detecção de Mãos e Cabeça", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

release_video_capture(cap)
