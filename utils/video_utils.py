import cv2

def start_video_capture():
    cap = cv2.VideoCapture(0)
    return cap

def release_video_capture(cap):
    cap.release()
    cv2.destroyAllWindows()
