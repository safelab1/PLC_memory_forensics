# pattern repeating at 0x4000 0040 th byte after every 0x80 bytes
import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)
jlink.connect('LPC2132')

starting_addr = 0x40000000 + 0x40
ending_addr = 0x4000FFFF

addr = starting_addr
a = jlink.memory_read(addr,01)
print a

i=1
j=1
k = 0x10000
while (addr +i*0x40) < ending_addr:
    time.sleep(0.01)
    b = jlink.memory_read(addr + i*0x80,01)
    print b
    if a!=b:
        a = jlink.memory_read(addr +(i-1)*0x80,01) # To confirm if both values are still not in sync
        print " This is a again " + str((a))
        if a !=b:
            b = jlink.memory_read(addr + i*0x80,01)
            print " Thi is b again " +(str(b))
            if a !=b:
                print ("False at " + str((i))) + " error count = " + str(j)
                j+=1
	a=b
    i+=1
print " Total  errors = " + j
