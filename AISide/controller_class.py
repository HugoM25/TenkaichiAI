'''
This class is used to store the inputs of a controller here the GameCube controller
'''

class GCInputs():

    def __init__(self) -> None:
        '''
        Initialize the inputs of the controller
        '''

        self.Left: int = 0
        self.Right: int = 0
        self.Down: int = 0
        self.Up: int = 0
        self.Z: int = 0
        self.R: int = 0
        self.L: int = 0
        self.A: int = 0
        self.B: int = 0
        self.X: int = 0
        self.Y: int = 0
        self.Start: int = 0
        self.StickX: int = 128 # 0-255, 128 is neutral 
        self.StickY: int = 128 # 0-255, 128 is neutral
        self.CStickX: int = 128 # 0-255, 128 is neutral
        self.CStickY: int = 128 # 0-255, 128 is neutral
        self.TriggerLeft: int = 255 # 0-255
        self.TriggerRight: int = 255 # 0-255
        self.AnalogA: int = 255 # 0-255
        self.AnalogB: int =255 # 0-255
        self.Connected: int = 0
    
    def parse_infos_json(self, data) -> None:
        '''
        Parse the json file containing the inputs of the controller
        '''
        self.Left = data['Left']
        self.Right = data['Right']
        self.Down = data['Down']
        self.Up = data['Up']
        self.Z = data['Z']
        self.R = data['R']
        self.L = data['L']
        self.A = data['A']
        self.B = data['B']
        self.X = data['X']
        self.Y = data['Y']
        self.Start = data['Start']
        self.StickX = data['StickX']
        self.StickY = data['StickY']
        self.CStickX = data['CStickX']
        self.CStickY = data['CStickY']
        self.TriggerLeft = data['TriggerLeft']
        self.TriggerRight = data['TriggerRight']
        self.AnalogA = data['AnalogA']
        self.AnalogB = data['AnalogB']
        self.Connected = data['Connected']
