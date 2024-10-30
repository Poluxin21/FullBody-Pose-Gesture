from config.dependencies import get_face_mesh
from services.head_service import calculate_head_movement

def process_head_landmarks(frame_rgb, frame_width, frame_height):
    face_mesh = get_face_mesh()
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            return calculate_head_movement(face_landmarks, frame_width, frame_height)
    return None
