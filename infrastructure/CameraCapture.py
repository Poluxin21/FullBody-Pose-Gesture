import cv2

class CameraCapture:
    def __init__(self, width=1280, height=720):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, width)
        self.cap.set(4, height)

    def get_frame(self):
        success, img = self.cap.read()
        return img if success else None
