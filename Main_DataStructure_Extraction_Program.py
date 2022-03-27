# Creating main datastructure for tags used in the program logic
# Jan 7,2020
# Following fields are used :-
##1) Tag assignment address : The address after 8000000A (for 1st tag, the value is stored at 0027FE5C
##2) Tag Description
##3) Tag address that stores data - the address is also used to compute logic region
##4) Tag type : control tag or program tag
##5) Firmware addr associated (should relate to some function in the firmware)
##6) Tag's current value (where applicable)
##7) Tag length (like SINT = 1 bytes, INT = 2 bytes, DINT = 4)

import pylink
import time
from Little_endian_conversions import *


jlink = pylink.JLink()
jlink.open(-1)
jlink.connect('LPC2132')

addr_cTag_asg_zone = 0x0027FE3C
addr_ControlLogic_end = 0x0027FE5C

######################################
## Methods

# byteArray_to_LE_string(a)
#byteArray_to_LE_int(a)
 
##########

coreDT = []

control_tag_start = byteArray_to_LE_int(jlink.memory_read(addr_cTag_asg_zone,4)) - 4 # minus 4 to point to the header
print hex(control_tag_start)

# Flow:
# We start with the control tag beginning and go down to cover all control tags
# During each dt of 40 bytes from 8000000A to 8000000A, we also fetch the tag description
# During the first entry, we fetch the border of the "control tag description" and use it in next section to fetch
# the program tags

# Condition to check if more dts are present: 8000000A followed by 8000000A


##############
# Section 1: control Tags
#############
# coreDT[][0] -> Tag description addres  - 9th dword
# coreDT[][1] -> Tag description - by fetching the contents at coreDT[x][0]
# coreDT[][2] -> Tag address - hex string 4 bytes LE - part of 40 bytes section 1 dt - 4th of the 10 dword
# coreDT[][3] -> Address where tag' address is found - points to the address of 4th dword
# coreDT[][4] -> Tag type - could be 'task', 'prog', routine, io_tag, others
# coreDT[][5] -> Tag data size - found in later sections
# coreDT[][6] -> Current value of tag - by fetching the contents at the address mentioned at coreDT[][2]
# coreDT[][7] -> Firmware address associated with tag - part of 40 bytes section 1 dt - 2nd of the 10 dword

#Tag_types
tag_io = 'IO_TAG'
tag_task = 'Task'
tag_prog = 'Program'
tag_routine = 'Routine'
tag_other = 'Others'
coreDT.append([])
coreDT[0]=('DES_ADDR','TAG_DES','TAG_ADDR','ADDR_TAG_ADDR',' TAG_TYPE ', 'TAG_DATA_SIZE','TAG_VALUE','FIRMWARE_ADDR')
fetched_seq = jlink.memory_read(control_tag_start,4)
tag_alloc_seq = [0x0A,0,0,0x80]
tag_count=0
if tag_alloc_seq!= fetched_seq:  # 0A 00 00 80
    print "The address pointer at " + str(addr_cTag_asg_zone) + " is not pointing to the correct location "
else:
    print "Going good"
    i = control_tag_start
    while jlink.memory_read(i,4) == tag_alloc_seq:
        tag_count+=1
        tag_dt = jlink.memory_read(i,40)
        coreDT.append([[],[],[],[],[],[],[],[]])
        coreDT[-1][0] = byteArray_to_LE_string(tag_dt[32:36])
        coreDT[-1][7] = byteArray_to_LE_string(tag_dt[4:8])
        coreDT[-1][2] = byteArray_to_LE_string(tag_dt[12:16])
        tag_des_size = jlink.memory_read(int(byteArray_to_LE_int(tag_dt[32:36])),1)[0]
        tag_des_array = jlink.memory_read(int(byteArray_to_LE_int(tag_dt[32:36]))+1,tag_des_size)
        tag_string = ''
        for x in tag_des_array:
            tag_string = tag_string + str(unichr(x))
        coreDT[-1][1] = tag_string
        coreDT[-1][3] = str(hex(i+ 12))[2:].zfill(8)
        if tag_count==1:
            lastProgTagStartAddr = int(coreDT[-1][0],16)-44  # Last program tag starting address
        
        i+=40 # next tag assignment dt
    for x in coreDT:
        print x
        
        
#######################################################
# SECTION 2 PROGRAM TAGS: 0A dts of different programs can be located at different locations

addr_ControlLogic_end
print hex(lastProgTagStartAddr)

i = lastProgTagStartAddr
while jlink.memory_read(i,4) == tag_alloc_seq:
    tag_count+=1
    tag_dt = jlink.memory_read(i,40)
    coreDT.append([[],[],[],[],[],[],[],[]])
    coreDT[-1][0] = byteArray_to_LE_string(tag_dt[32:36])
    coreDT[-1][7] = byteArray_to_LE_string(tag_dt[4:8])
    coreDT[-1][2] = byteArray_to_LE_string(tag_dt[12:16])
    tag_des_size = jlink.memory_read(int(byteArray_to_LE_int(tag_dt[32:36])),1)[0]
    tag_des_array = jlink.memory_read(int(byteArray_to_LE_int(tag_dt[32:36]))+1,tag_des_size)
    tag_string = ''
    for x in tag_des_array:
        tag_string = tag_string + str(unichr(x))
    coreDT[-1][1] = tag_string
    coreDT[-1][3] = str(hex(i+ 12))[2:].zfill(8)
    
    i-=40

for x in coreDT:
    print x


###################################################################
# SECTION 3 CONTROL LOGIC

# the pointer at 0027FE5C points to start of a dt with header "80000031"
# our interest is in dt 2 up than this one.






jlink.close()
