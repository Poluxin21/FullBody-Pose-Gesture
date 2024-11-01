from infrastructure.CameraCapture import CameraCapture
from infrastructure.HandDetectorAdapter import HandDetectorAdapter
from infrastructure.SocketAdapter import SocketAdapter
from application.HandTrackingService import HandTrackingService
from interface.HandTrackingApp import HandTrackingApp
from infrastructure.CompilerAndExecute import CppCompiler

def main():
    camera = CameraCapture()
    detector = HandDetectorAdapter()
    socket_adapter = SocketAdapter()

    tracking_service = HandTrackingService(detector, camera, socket_adapter)
    app = HandTrackingApp(tracking_service)

    app.run()

if __name__ == "__main__":
    cpp_file = "src/vrDriver/main.cpp"
    executable = "src/vrDriver/main"
    include_dir = "src/vrDriver/openvr-2.5.1"
    lib_name = "openvr_api"

    compiler = CppCompiler(cpp_file, executable, include_dir, lib_name)
    compiler.compile_and_run()
    
    main()
