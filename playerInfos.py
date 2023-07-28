import dolphin_memory_engine as dme 
from utils import read_bytes

class PlayerInfos : 

    def __init__(self, name="P1") -> None:
        self.health = 0
        self.ki = 0
        self.full_power_bar = 0
        self.transfo = 0
        self.name = name

    def get_values(self, 
                   addr_health, 
                   addr_ki, 
                   addr_full_power_bar, 
                   addr_transfo, 
                   addr_pos_x, 
                   addr_pos_y, 
                   addr_pos_z, 
                   addr_combo, 
                   addr_att_b_cnt, 
                   addr_att_b_flag, 
                   addr_att_k_cnt) :
        
        self.health = read_bytes(addr_health, 2)
        self.ki = read_bytes(addr_ki, 2)
        self.full_power_bar = read_bytes(addr_full_power_bar, 2)
        self.transfo = read_bytes(addr_transfo, 3)
        self.pos_x = dme.read_float(addr_pos_x)
        self.pos_y = dme.read_float(addr_pos_y)
        self.pos_z = dme.read_float(addr_pos_z)
        self.att_b_cnt = dme.read_byte(addr_att_b_cnt)
        self.att_b_flag = dme.read_byte(addr_att_b_flag)
        self.combo = dme.read_byte(addr_combo)
        self.att_k_cnt = dme.read_byte(addr_att_k_cnt)

    
    def log(self) -> None : 
        print(f'health {self.name} : {self.health}')
        print(f'ki {self.name} : {self.ki}')
        print(f'transfo {self.name} : {self.transfo}')
        print(f'full power bar {self.name} : {self.full_power_bar}')
        print(f"pos is x={self.pos_x} y={self.pos_y} z={self.pos_z}")
        print(f"{self.name} is doing a combo of {self.combo}")

        if self.att_b_flag : 
            print(f"{self.name} is pressing the base atk for the {self.att_b_cnt} time")
        
        if self.att_k_cnt > 0 : 
            print(f"{self.name} is pressing the ki atk for the {self.att_k_cnt} time")
