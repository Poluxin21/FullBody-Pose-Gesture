import socket
import threading
import time
import pyopenxr as xr
import numpy as np

class XRDeviceController:
    def __init__(self, ip="127.0.0.1", port=5052):
        self.instance = xr.create_instance()
        self.system = self.instance.get_system(xr.FormFactor.HeadMountedDisplay)
        self.session = self.instance.create_session(self.system)
        self.input = self.session.create_input()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.running = True

    def receive_data(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(1024)
                values = list(map(float, data.decode().split(',')))

                if len(values) == 7:
                    position = values[:3]
                    rotation = values[3:]
                    self.update_vr_device(position, rotation)
                else:
                    print("Dados inválidos recebidos:", data)

            except Exception as e:
                print(f"Erro ao receber dados: {e}")

    def update_vr_device(self, position, rotation):
        try:
            transformation_matrix = self.build_transformation_matrix(position, rotation)
            self.update_hmd_pose(transformation_matrix)

        except Exception as e:
            print(f"Erro ao atualizar o dispositivo VR: {e}")

    def update_hmd_pose(self, matrix):
        try:
            hmd = self.input.get_device(xr.InputSource.Head)
            hmd.pose = matrix
            self.session.update_device(hmd)
        except Exception as e:
            print(f"Erro ao atualizar HMD: {e}")

    def build_transformation_matrix(self, position, rotation):
        x, y, z = position
        qx, qy, qz, qw = rotation
        return np.array([
            [1 - 2*qy*qy - 2*qz*qz, 2*qx*qy - 2*qz*qw, 2*qx*qz + 2*qy*qw, x],
            [2*qx*qy + 2*qz*qw, 1 - 2*qx*qx - 2*qz*qz, 2*qy*qz - 2*qx*qw, y],
            [2*qx*qz - 2*qy*qw, 2*qy*qz + 2*qx*qw, 1 - 2*qx*qx - 2*qy*qy, z],
            [0, 0, 0, 1]
        ])

    def start(self):
        self.thread = threading.Thread(target=self.receive_data)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.sock.close()
        self.session.shutdown()
        self.instance.shutdown()

