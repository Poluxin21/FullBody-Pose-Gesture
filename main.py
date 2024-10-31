from infrastructure.CameraCapture import CameraCapture
from infrastructure.HandDetectorAdapter import HandDetectorAdapter
from infrastructure.SocketAdapter import SocketAdapter
from application.HandTrackingService import HandTrackingService
from interface.HandTrackingApp import HandTrackingApp

def main():
    camera = CameraCapture()
    detector = HandDetectorAdapter()
    socket_adapter = SocketAdapter()

    tracking_service = HandTrackingService(detector, camera, socket_adapter)
    app = HandTrackingApp(tracking_service)

    app.run()

if __name__ == "__main__":
    main()
