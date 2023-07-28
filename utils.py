import dolphin_memory_engine as dme

def combine_hex_values(num1, num2):
    '''
    Combine two hex values into one
    @param num1: first hex value
    @param num2: second hex value
    @return: combined hex value
    '''
    hex_value = (num1 << 8) | num2
    return hex_value

def read_bytes(address, num_bytes) : 
    '''
    Read a number of bytes from a given address
    @param address: address to read from
    @param num_bytes: number of bytes to read
    @return: value read
    '''
    val_read = 0x0
    for i in range(0, num_bytes) :
        address += i
        hex_of_byte = dme.read_byte(address)
        val_read = combine_hex_values(val_read, hex_of_byte)
    return val_read
