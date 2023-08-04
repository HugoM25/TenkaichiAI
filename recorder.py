from dolphin import event, gui, controller, memory
import json

red = 0xffff0000

# List of addresses containing useful dbzbt3 informations
# The list is incomplete and needs more infos 
# But it's already quite nice 

# 1 byte 
TIMER_MEM = 0x92343BEF

# 2 bytes for most health bar (may be more, have to check)
HEALTH_P1_MEM = 0x92334CA2
HEALTH_P2_MEM = 0x92336D42

# 3 bytes
TRANSFO_P1 = 0x92334CB5
TRANSFO_P2 = 0x923428D1

# 2 bytes
FULL_POWER_P1 = 0x92334CBE
FULL_POWER_P2 = 0x92336D5E

# 2 bytes
KI_P1 = 0x92334CAE
KI_P2 = 0x92336D4E

# Positions are floats 
POS_X_P1 = 0x90F9A570
POS_Y_P1 = 0x90F9A004
POS_Z_P1 = 0x90F99F48

POS_X_P2 = 0x90F9B5D0
POS_Y_P2 = 0x90F9B694
POS_Z_P2 = 0x90F9B608

# 1 byte
ATTACK_BASE_P1_FLAG = 0x9233537E
ATTACK_BASE_P1_CNT  = 0x9233501F

ATTACK_BASE_P2_FLAG = 0x9233741E
ATTACK_BASE_P2_CNT =  0x923370BF

ATTACK_KI_P1_CNT =  0x923350A3
ATTACK_KI_P2_CNT =  0x92337143


#1 byte 
COMBO_P1 = 0x92344CB3
COMBO_P2 = 0x92344CB



class ObsEnv:
    def __init__(self):

        self.P1_X = 0
        self.P1_Y = 0
        self.P1_Z = 0
        self.P2_X = 0
        self.P2_Y = 0
        self.P2_Z = 0 

        self.P1_health = 0
        self.P2_health = 0

        self.P1_ki = 0
        self.P2_ki = 0

        self.P1_transfo = 0
        self.P2_transfo = 0

        self.P1_full_power = 0
        self.P2_full_power = 0

        self.P1_press_base_attack_flag = 0
        self.P2_press_base_attack_flag = 0

        self.P1_press_base_attack_cnt = 0
        self.P2_press_base_attack_cnt = 0

        self.P1_press_ki_attack_cnt = 0
        self.P2_press_ki_attack_cnt = 0

        self.timer = 0

        self.P1_combo = 0
        self.P2_combo = 0
    
# Reset sample.json
with open("sample.json", "w") as outfile:
    outfile.write("")

def record_frame():
    # Get observation
    obs = get_obs()
    dict_obs = obs.__dict__

    # Get controller input
    controller_inputs_obj = controller.get_gc_buttons(0)
    dict_controller = dict(controller_inputs_obj) 

    # combine both inside "record" item json (both are dict)
    json_record = {"obs": dict_obs, "controller": dict_controller}

    # Add item to sample.json
    with open("sample.json", "a") as outfile:
        json_obj = json.dumps(json_record)
        outfile.write(json_obj + ",\n")

    # Write 
    gui.draw_text((10, 10), red, f"Saved at: here")


def get_obs() -> ObsEnv:
    obs = ObsEnv()
    # Read Position
    obs.P1_X = memory.read_f32(POS_X_P1)
    obs.P1_Y = memory.read_f32(POS_Y_P1)
    obs.P1_Z = memory.read_f32(POS_Z_P1)

    obs.P2_X = memory.read_f32(POS_X_P2)
    obs.P2_Y = memory.read_f32(POS_Y_P2)
    obs.P2_Z = memory.read_f32(POS_Z_P2)

    # Read Health
    obs.P1_health = memory.read_u16(HEALTH_P1_MEM)
    obs.P2_health = memory.read_u16(HEALTH_P2_MEM)

    # Read timer 
    obs.timer = memory.read_u8(TIMER_MEM)

    # Read Ki
    obs.P1_ki = memory.read_u16(KI_P1)
    obs.P2_ki = memory.read_u16(KI_P2)

    # Read Transfo
    obs.P1_transfo = memory.read_u32(TRANSFO_P1)
    obs.P2_transfo = memory.read_u32(TRANSFO_P2)

    # Read Full Power
    obs.P1_full_power = memory.read_u16(FULL_POWER_P1)
    obs.P2_full_power = memory.read_u16(FULL_POWER_P2)

    # Read Attack
    obs.P1_press_base_attack_flag = memory.read_u8(ATTACK_BASE_P1_FLAG)
    obs.P2_press_base_attack_flag = memory.read_u8(ATTACK_BASE_P2_FLAG)

    obs.P1_press_base_attack_cnt = memory.read_u8(ATTACK_BASE_P1_CNT)
    obs.P2_press_base_attack_cnt = memory.read_u8(ATTACK_BASE_P2_CNT)

    obs.P1_press_ki_attack_cnt = memory.read_u8(ATTACK_KI_P1_CNT)
    obs.P2_press_ki_attack_cnt = memory.read_u8(ATTACK_KI_P2_CNT)


    # Read combo
    obs.P1_combo = memory.read_u8(COMBO_P1)
    obs.P2_combo = memory.read_u8(COMBO_P2)

    return obs

frame_count = 0

while True:
    await event.frameadvance()

    if frame_count >= 10:
        record_frame()
        frame_count = 0
    
    frame_count += 1
    
