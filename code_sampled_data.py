import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)

jlink.connect('LPC2132')
f = open("sampled_data2.txt","a+") # change the number after data
starting_address= 0x20000000  # Enter the starting address here
start_decimal = int(starting_address)
for i in range(0,10000000):
    a = jlink.memory_read(start_decimal + i*2048,16)
    b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if a!=b:
        d = hex(start_decimal + i*2048)
        f.write(d)
        f.write(",")
        #f.write(b'\x01\x01\x01')
        print(d)
        print(a)
        f.write(bytearray(a))
        time.sleep(0.5)
        if i%100 == 0:
            f.close()
            time.sleep(0.1)
            f = open("sampled_data2.bin","a+")
f.close()
    
