'''
This class is used to store the inputs of a controller here the GameCube controller
'''

class GCInputs():

    def __init__(self) -> None:
        '''
        Initialize the inputs of the controller
        '''

        self.Left: bool = False
        self.Right: bool = False
        self.Down: bool = False
        self.Up: bool  = False
        self.Z: bool = False
        self.R: bool = False
        self.L: bool = False
        self.A: bool = False
        self.B: bool = False
        self.X: bool = False
        self.Y: bool = False
        self.Start: bool = False
        self.StickX: int = 128 # 0-255, 128 is neutral 
        self.StickY: int = 128 # 0-255, 128 is neutral
        self.CStickX: int = 128 # 0-255, 128 is neutral
        self.CStickY: int = 128 # 0-255, 128 is neutral
        self.TriggerLeft: int = 255 # 0-255
        self.TriggerRight: int = 255 # 0-255
        self.AnalogA: int = 255 # 0-255
        self.AnalogB: int =255 # 0-255
        self.Connected: bool = True
    
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
