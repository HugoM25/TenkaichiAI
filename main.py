import dolphin_memory_engine as dme
import time 
from const import * 
from env import Env

def main() : 
    #Hook dolphin 
    dme.hook()

    #Check the hook
    if dme.is_hooked() != True :
        print("Could not hook")
        return
    
    env = Env()

    while dme.is_hooked() :
        env.update_values()
        env.p1_infos.log()
        env.p2_infos.log()
        print(f"timer : {env.timer}")
        time.sleep(1)
    

if __name__ == "__main__" :
    main()