class HandData:
    def __init__(self, landmarks):
        self.landmarks = landmarks
    
    def to_network_format(self):

        palm = self.landmarks[0]
        index_tip = self.landmarks[8]

        palm_x, palm_y, palm_z = palm[0], palm[1], palm[2]
        index_x, index_y, index_z = index_tip[0], index_tip[1], index_tip[2]

        return {
            "/avatar/parameters/RightHandPalmX": palm_x,
            "/avatar/parameters/RightHandPalmY": palm_y,
            "/avatar/parameters/RightHandPalmZ": palm_z,
            "/avatar/parameters/RightIndexTipX": index_x,
            "/avatar/parameters/RightIndexTipY": index_y,
            "/avatar/parameters/RightIndexTipZ": index_z
        }
