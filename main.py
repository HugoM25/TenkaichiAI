import dolphin_memory_engine as dme
import time 
import pyautogui

from const import * 


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


def combine_hex_values(num1, num2):
    hex_value = (num1 << 8) | num2
    return hex_value

def read_bytes(address, num_bytes) : 
    val_read = 0x0
    for i in range(0, num_bytes) :
        address += i
        hex_of_byte = dme.read_byte(address)
        val_read = combine_hex_values(val_read, hex_of_byte)
    return val_read

def main() : 
    #Hook dolphin 
    dme.hook()

    #Check the hook
    if dme.is_hooked() != True :
        print("Could not hook")
        return
    
    p1_infos = PlayerInfos("P1")
    p2_infos = PlayerInfos("P2")

    while dme.is_hooked() :
        #While hooked read values from memory 
        p1_infos.get_values(HEALTH_P1_MEM, 
                            KI_P1, 
                            FULL_POWER_P1, 
                            TRANSFO_P1, 
                            POS_X_P1, POS_Y_P1, POS_Z_P1, 
                            COMBO_P1, 
                            ATTACK_BASE_P1_CNT, 
                            ATTACK_BASE_P1_FLAG, 
                            ATTACK_KI_P1_CNT)
        
        p2_infos.get_values(HEALTH_P2_MEM, 
                            KI_P2, 
                            FULL_POWER_P2, 
                            TRANSFO_P2, 
                            POS_X_P2, POS_Y_P2, POS_Z_P2, 
                            COMBO_P2, 
                            ATTACK_BASE_P2_CNT, 
                            ATTACK_BASE_P2_FLAG, 
                            ATTACK_KI_P2_CNT)
        
        timer = dme.read_byte(TIMER_MEM)

        #Display them 
        print("-----------------")
        print(f"timer : {timer}")
        p1_infos.log()
        p2_infos.log()
        print("-----------------")

        time.sleep(0.5)

        if (p1_infos.health == 0 or p2_infos.health == 0 or timer == 0):
            #Cut episode and restart the fight
            pyautogui.keyDown('f1')
            print("Restart env...")
            time.sleep(1)
        


if __name__ == "__main__" :
    main()