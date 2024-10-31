from domain.HandData import HandData

class HandTrackingService:
    def __init__(self, detector, camera, socket_adapter):
        self.detector = detector
        self.camera = camera
        self.socket_adapter = socket_adapter

    def process_frame(self):
        img = self.camera.get_frame()
        hands = self.detector.detect_hands(img)
        
        if hands:
            for hand in hands:
                hand_data = HandData(hand['lmList'])
                self.socket_adapter.send(hand_data.to_network_format())
                
        return img
