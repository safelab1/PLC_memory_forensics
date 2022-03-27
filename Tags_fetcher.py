import pylink
import time
from Little_endian_conversions import *



## Receives coreDT, pointer pointing to the 2nd dword after 8000000A, and the scope (like controller or program:programMain
# Fetches all the tags in the region
# and returns the updated coreDT

def fetch_tags(coreDT, start_pointer, scope):
##    print scope
    time.sleep(1)
    jlink = pylink.JLink()
    jlink.open(-1)
    jlink.connect('LPC2132')
    tag_alloc_seq = [0x0A,0,0,0x80]
##    print start_pointer
    tag_start = int(start_pointer,16)-4 #  -4 to take to 8000000A
##    print tag_start
    fetched_seq = jlink.memory_read(tag_start,4)
##    print fetched_seq
    if tag_alloc_seq!= fetched_seq:  # 0A 00 00 80
        print "The address pointer at " + start_pointer + " is not pointing to the correct location "
    else:
##        print "Going good"
        i = tag_start
        while jlink.memory_read(i,4) == tag_alloc_seq:
            tag_dt = jlink.memory_read(i,40)
            coreDT.append([[],[],[],[],[],[],[],[],[]])
            coreDT[-1][0] = byteArray_to_LE_string(tag_dt[32:36])
            coreDT[-1][8] = byteArray_to_LE_string(tag_dt[4:8])
            coreDT[-1][2] = byteArray_to_LE_string(tag_dt[12:16])
            coreDT[-1][4] = scope
            tag_des_size = jlink.memory_read((byteArray_to_LE_int(tag_dt[32:36])),1)[0]
            tag_des_array = jlink.memory_read((byteArray_to_LE_int(tag_dt[32:36]))+1,tag_des_size)
            tag_string = ''
            for x in tag_des_array:
                tag_string = tag_string + str(unichr(x))
            coreDT[-1][1] = tag_string
            coreDT[-1][3] = str(hex(i+ 12))[2:].zfill(8)
             
            i+=40 # next tag assignment dt
    jlink.close()
    return coreDT
