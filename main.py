import traceback
from infrastructure.CameraCapture import CameraCapture
from infrastructure.HandDetectorAdapter import HandDetectorAdapter
from infrastructure.SocketAdapter import SocketAdapter
from infrastructure.VRDeviceController import VRDeviceController
from application.HandTrackingService import HandTrackingService
from interface.HandTrackingApp import HandTrackingApp
from infrastructure.XRDeviceController import XRDeviceController

def main():
    try:
        camera = CameraCapture()
        print("Camera inicializada com sucesso.")
        detector = HandDetectorAdapter()
        print("Detector de mão inicializado com sucesso.")
        socket_adapter = SocketAdapter()
        print("Adaptador de socket inicializado com sucesso.")
        vr_controller = VRDeviceController()
        print("Controlador VR (OpenVR) inicializado com sucesso.")
        
        # TIRAR OS COMENTARIOS CASO QUEIRA USAR OpenXR
        # xr_controller = XRDeviceController()
        # print("Controlador VR (OpenXR) inicializado com sucesso.")
    
        tracking_service = HandTrackingService(detector, camera, socket_adapter)
        app = HandTrackingApp(tracking_service)

        vr_controller.start()

        # xr_controller.start()

        try:
            app.run()
        finally:
            vr_controller.stop()

    except Exception as e:
        print("Erro durante a execução:")
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
