import openvr
import socket
import struct
import threading
import time

class VRDeviceController:
    def __init__(self, ip="127.0.0.1", port=5052):
        # Inicializa o OpenVR
        openvr.init(openvr.VRApplication_Scene)
        
        # Configuração do socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.running = True

    def receive_data(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(1024)
                # Decodifica a string recebida e converte em floats (exemplo: "x,y,z,rx,ry,rz,rw")
                values = list(map(float, data.decode().split(',')))

                if len(values) == 7:  # Exemplo: (x, y, z, qx, qy, qz, qw)
                    position = values[:3]
                    rotation = values[3:]
                    self.update_vr_device(position, rotation)
                else:
                    print("Dados inválidos recebidos:", data)

            except Exception as e:
                print(f"Erro ao receber dados: {e}")

    def update_vr_device(self, position, rotation):
        try:
            hmd_pose = openvr.VRInputComponentHandle_t()
            
            # Define a matriz de transformação com posição e orientação
            pose = openvr.TrackedDevicePose_t()
            pose.mDeviceToAbsoluteTracking = self.build_transformation_matrix(position, rotation)
            
            # Atualiza a pose do dispositivo de VR
            openvr.VRSystem().resetSeatedZeroPose()
            openvr.VRCompositor().submit(openvr.Eye_Left, pose, None, openvr.Submit_Default)
            openvr.VRCompositor().submit(openvr.Eye_Right, pose, None, openvr.Submit_Default)
        except Exception as e:
            print(f"Erro ao atualizar o dispositivo VR: {e}")

    def build_transformation_matrix(self, position, rotation):
        x, y, z = position
        qx, qy, qz, qw = rotation

        # Matriz de transformação baseada em quaternions
        return [
            [1 - 2*qy*qy - 2*qz*qz, 2*qx*qy - 2*qz*qw, 2*qx*qz + 2*qy*qw, x],
            [2*qx*qy + 2*qz*qw, 1 - 2*qx*qx - 2*qz*qz, 2*qy*qz - 2*qx*qw, y],
            [2*qx*qz - 2*qy*qw, 2*qy*qz + 2*qx*qw, 1 - 2*qx*qx - 2*qy*qy, z],
            [0, 0, 0, 1]
        ]

    def start(self):
        self.thread = threading.Thread(target=self.receive_data)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        openvr.shutdown()
        self.sock.close()
