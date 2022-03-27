import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)
jlink.connect('LPC2132')

starting_addr = 0x00700000
ending_addr = 0x00CFFFFF


# fetch a word; is it non-zero? give address, else jump 4KB (0x1000)

i=starting_addr

while i < ending_addr-16 :
    a = jlink.memory_read(i,16)
    for x in a:
        if x != 0:
            print i
    i+=0x1000
