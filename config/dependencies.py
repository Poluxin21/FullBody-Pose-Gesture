import mediapipe as mp
import pyvjoy

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)
vjoy_device = pyvjoy.VJoyDevice(1)  # Inicialize o dispositivo VJoy

def get_vjoy_device():
    return vjoy_device

def get_hands():
    return hands

def get_face_mesh():
    return face_mesh
