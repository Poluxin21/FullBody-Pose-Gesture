from infrastructure.CameraCapture import CameraCapture
from infrastructure.HandDetectorAdapter import HandDetectorAdapter
from infrastructure.SocketAdapter import SocketAdapter
from application.HandTrackingService import HandTrackingService
from interface.HandTrackingApp import HandTrackingApp
from infrastructure.VRDeviceController import VRDeviceController

def main():
    # Inicialização dos componentes
    camera = CameraCapture()
    detector = HandDetectorAdapter()
    socket_adapter = SocketAdapter()
    vr_controller = VRDeviceController()

    tracking_service = HandTrackingService(detector, camera, socket_adapter)
    app = HandTrackingApp(tracking_service)
    
    vr_controller.start()

    try:
        app.run()
    finally:
        vr_controller.stop()

if __name__ == "__main__":
    main()
