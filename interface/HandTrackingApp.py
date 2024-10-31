import cv2

class HandTrackingApp:
    def __init__(self, tracking_service):
        self.tracking_service = tracking_service

    def run(self):
        while True:
            img = self.tracking_service.process_frame()
            if img is not None:
                cv2.imshow("Hand Tracking", img)
                if cv2.waitKey(1) == ord('q'):
                    break
        cv2.destroyAllWindows()
