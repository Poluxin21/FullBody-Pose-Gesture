class HandData:
    def __init__(self, landmarks):
        self.landmarks = landmarks 
    
    def to_network_format(self):
        return str(self.landmarks)
