import dolphin_memory_engine as dme
import time 
import pyautogui

#MEM VALUES ADDRESSES
#1 byte 
TIMER_MEM = int('92343BEF', 16)

# 2 bytes for most health bar (may be more, have to check)
HEALTH_P1_MEM = int('92334CA2', 16)
HEALTH_P2_MEM = int('92336D42', 16)

# 3 bytes
TRANSFO_P1 = int('92334CB5', 16)
TRANSFO_P2 = int('923428D1', 16)

# 2 bytes
FULL_POWER_P1 = int('92334CBE', 16)
FULL_POWER_P2 = int('92336D5E', 16)

# 2 bytes
KI_P1 = int('92334CAE', 16)
KI_P2 = int('92336D4E', 16)

class PlayerInfos : 

    def __init__(self, name="P1") -> None:
        self.health = 0
        self.ki = 0
        self.full_power_bar = 0
        self.transfo = 0
        self.name = name

    def get_values(self, addr_health, addr_ki, addr_full_power_bar, addr_transfo) :
        self.health = read_bytes(addr_health, 2)
        self.ki = read_bytes(addr_ki, 2)
        self.full_power_bar = read_bytes(addr_full_power_bar, 2)
        self.transfo = read_bytes(addr_transfo, 3)
    
    def log(self) -> None : 
        print(f'health {self.name} : {self.health}')
        print(f'ki {self.name} : {self.ki}')
        print(f'transfo {self.name} : {self.transfo}')
        print(f'full power bar {self.name} : {self.full_power_bar}')

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
        p1_infos.get_values(HEALTH_P1_MEM, KI_P1, FULL_POWER_P1, TRANSFO_P1)
        p2_infos.get_values(HEALTH_P2_MEM, KI_P2, FULL_POWER_P2, TRANSFO_P2)
        timer = dme.read_byte(TIMER_MEM)

        #Display them 
        print("-----------------")
        print(f"timer : {timer}")
        p1_infos.log()
        p2_infos.log()
        print("-----------------")

        time.sleep(1)

        if (p1_infos.health == 0 or p2_infos.health == 0 or timer == 0):
            #Cut episode and restart the fight
            pyautogui.keyDown('f1')
            print("Restart env...")
            time.sleep(1)
        


if __name__ == "__main__" :
    main()