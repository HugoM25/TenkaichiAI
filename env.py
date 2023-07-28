import dolphin_memory_engine as dme
from const import *
from playerInfos import PlayerInfos

class Env : 

    def __init__(self) -> None:
        self.p1_infos = PlayerInfos("P1")
        self.p2_infos = PlayerInfos("P2")
        self.timer = 0

    def update_values(self) -> None : 
        '''
        Update the values from memory
        @return : None
        '''
        self.p1_infos.get_values(HEALTH_P1_MEM, 
                    KI_P1, 
                    FULL_POWER_P1, 
                    TRANSFO_P1, 
                    POS_X_P1, POS_Y_P1, POS_Z_P1, 
                    COMBO_P1, 
                    ATTACK_BASE_P1_CNT, 
                    ATTACK_BASE_P1_FLAG, 
                    ATTACK_KI_P1_CNT)

        self.p2_infos.get_values(HEALTH_P2_MEM, 
                    KI_P2, 
                    FULL_POWER_P2, 
                    TRANSFO_P2, 
                    POS_X_P2, POS_Y_P2, POS_Z_P2, 
                    COMBO_P2, 
                    ATTACK_BASE_P2_CNT, 
                    ATTACK_BASE_P2_FLAG, 
                    ATTACK_KI_P2_CNT)
        
        self.timer = dme.read_byte(TIMER_MEM)
        
    def reset_env(self) -> None : 
        '''
        Cut episode and restart the fight by loading a save state
        @return : None
        '''
        print("Restart env...")