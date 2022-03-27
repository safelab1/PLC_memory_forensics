
import pylink
import time

###############################################################
def indexInArray( to_match_this, in_this_array):
    for i in range (len(in_this_array) - len(to_match_this)+1):
        for j in range(len(to_match_this)):
            if to_match_this[j] != in_this_array[i+j]:
                break
        else:
            #if(i)%4 == 0:
                return i
    return -1

##############################################333

jlink = pylink.JLink()
jlink.open(-1)
jlink.connect('LPC2132')

start_addr = 0x00278000
end_addr = 0x00279A00
io_address = [0x40,0x00,0x0c]
chunksize = 256
i = start_addr

while i < end_addr:
    time.sleep(2)
    a=jlink.memory_read(i,chunksize)
    #print a
    a = bytearray(a)
    x=indexInArray(io_address,a)
    #print x
    if x!=-1:
        print str(hex(i+x))
    i+=chunksize
        
      
