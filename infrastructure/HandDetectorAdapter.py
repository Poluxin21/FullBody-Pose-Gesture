from cvzone.HandTrackingModule import HandDetector

class HandDetectorAdapter:
    def __init__(self, max_hands=2, detection_confidence=0.8):
        self.detector = HandDetector(maxHands=max_hands, detectionCon=detection_confidence)

    def detect_hands(self, img):
        hands, img = self.detector.findHands(img, draw=True)
        return hands
