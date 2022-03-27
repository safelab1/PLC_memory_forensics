import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)
jlink.connect('LPC2132')

starting_addr = 0x70000000
ending_addr   = 0x7FFFFFFF


# fetch a word; is it non-zero? give address, else jump 4KB (0x1000)

i=starting_addr

while i < ending_addr :
    a = jlink.memory_read(i,1)
    time.sleep(0.5)
    if len(a)>0:
        print i
    i+=0x400
