# List of addresses containing useful dbzbt3 informations
# The list is incomplete and needs more infos 
# But it's already quite nice 

# 1 byte 
TIMER_MEM = int('92343BEF', 16)
TIMER_MEM_1 = int('92346535', 16) # same as TIMER_MEM
TIMER_MEM_2 = int('92343BF3', 16) # same as TIMER_MEM

# 2 bytes for most health bar (may be more, have to check)
HEALTH_P1_MEM = int('92334CA2', 16)
HEALTH_P2_MEM = int('92336D42', 16)

# 3 bytes
TRANSFO_P1 = int('92334CB5', 16)
TRANSFO_P2 = int('923428D1', 16)

# 2 bytes
FULL_POWER_P1 = int('92334CBE', 16)
FULL_POWER_P1_1 = int('92334CBE', 16) 
FULL_POWER_P2 = int('92336D5E', 16)

# 2 bytes
KI_P1 = int('92334CAE', 16)
KI_P2 = int('92336D4E', 16)

# Positions are floats 
POS_X_P1 = int('90F9A570', 16)
POS_Y_P1 = int('90F9A004', 16)
POS_Z_P1 = int('90F99F48', 16)

POS_X_P2 = int('90F9B5D0', 16)
POS_Y_P2 = int('90F9B694', 16)
POS_Z_P2 = int('90F9B608', 16)

# 1 byte
ATTACK_BASE_P1_FLAG = int('9233537E', 16)
ATTACK_BASE_P1_CNT  = int('9233501F', 16)

ATTACK_BASE_P2_FLAG = int('9233741E', 16)
ATTACK_BASE_P2_CNT =  int('923370BF', 16)

ATTACK_KI_P1_CNT =  int('923350A3', 16)
ATTACK_KI_P2_CNT =  int('92337143', 16)


#1 byte 
COMBO_P1 = int('92344CB3', 16)
COMBO_P2 = int('92344CB7', 16)

# 4 bytes
MAX_COMBO_DAMAGE_BY_P1 = 0x803D1014
MAX_COMBO_DAMAGE_BY_P2 = 0x803D1018

# 4 bytes
DAMAGE_TAKEN_COMBO_ON_P2 = 0x9233709C
DAMAGE_TAKEN_COMBO_ON_P2_1 = 0x92344C98
DAMAGE_TAKEN_COMBO_ON_P1 = 0x92344C9C

# 1 byte
SPEED = 0x92684CE3

# 128 - when fp
LIGHTNING_P1_FP = 0x9234289B
LIGHTNING_P2_FP = 0x9234289F

# 1 byte
# 128 - Round out
# 64-128 - FP P1
# 32-64 Normal
# 0-32 Lock on
STATE_FIGHT_P1 = 0x92335345


