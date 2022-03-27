# The setup needs a usb connection from this PC to Debugger that is connected to PLC on JTAG port
# In this implementation, we used Segger JLINK debugger connected to Allen-Bradley Control Logic 1756
# Jan 11,2020 : Multiple Program handling included(previous approach only cater single program)
# Jan 11,2020: Also added 'Tag_type' and 'tag_scope'
# Jan 7:
# Creating main datastructure for tags used in the program logic - 
# Following fields are used :-
##1) Tag assignment address : The address after 8000000A (for 1st tag, the value is stored at 0027FE5C
##2) Tag Description
##3) Tag address that stores data - the address is also used to compute logic region
##4) Tag type : control tag or program tag
##5) Firmware addr associated (should relate to some function in the firmware)
##6) Tag's current value (where applicable)
##7) Tag length (like SINT = 1 bytes, INT = 2 bytes, DINT = 4)
import sys
import pylink
import time
import msvcrt
jlink = pylink.JLink()
jlink.open(-1)
jlink.connect('LPC2132')

from Little_endian_conversions import *
from Tags_fetcher import *
from Instr_dictionary import INSTR_DICT


time_str = time.strftime("%Y%m%d-%H%M%S")
dest_folder = "./"


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

control_tag_start = byteArray_to_LE_string(jlink.memory_read(addr_cTag_asg_zone,4))  
print "Controller tag allocation zone starting at " + (control_tag_start)

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
# coreDT[][4] -> Tag scope - like controller, program:program1 etc
# coreDT[][5] -> Tag type - could be 'task', 'prog', routine, io_tag, others
# coreDT[][6] -> Tag data size - found in later sections
# coreDT[][7] -> Current value of tag - by fetching the contents at the address mentioned at coreDT[][2]
# coreDT[][8] -> Firmware address associated with tag - part of 40 bytes section 1 dt - 2nd of the 10 dword

#Tag_types
type_io = 'IO_TAG'
type_task = 'Task'
type_prog = 'Program'
type_routine = 'Routine'
type_other = 'Others'

#Firmware addresses for various tags types
faddr_program = '00f58108' # 8000005B
faddr_routine = '00f5c440' # 80000032
faddr_tag_asg = '00f55b3c' # 8000000A
faddr_tag_value= '00f54c54' # 80000007 or 80000008

tag_alloc_seq = [0x0A,0,0,0x80]

##fetched_seq = jlink.memory_read(control_tag_start,4)
coreDTheader=('DES_ADDR ','  TAG_DES  ','  TAG_ADDR   ',' ADDR_TAG_ADDR  ', ' TAG_SCOPE ', ' TAG_TYPE ', 'TAG_DATA_SIZE','TAG_VALUE','FIRMWARE_ADDR')

jlink.close()
coreDT = fetch_tags(coreDT,control_tag_start,"controller")
jlink.open(-1)
jlink.connect('LPC2132')

##tag_count=0
##if tag_alloc_seq!= fetched_seq:  # 0A 00 00 80
##    print "The address pointer at " + str(addr_cTag_asg_zone) + " is not pointing to the correct location "
##else:
##    print "Going good"
##    i = control_tag_start
##    while jlink.memory_read(i,4) == tag_alloc_seq:
##        tag_count+=1
##        tag_dt = jlink.memory_read(i,40)
##        coreDT.append([[],[],[],[],[],[],[],[],[]])
##        coreDT[-1][0] = byteArray_to_LE_string(tag_dt[32:36])
##        coreDT[-1][8] = byteArray_to_LE_string(tag_dt[4:8])
##        coreDT[-1][2] = byteArray_to_LE_string(tag_dt[12:16])
##        tag_des_size = jlink.memory_read((byteArray_to_LE_int(tag_dt[32:36])),1)[0]
##        tag_des_array = jlink.memory_read((byteArray_to_LE_int(tag_dt[32:36]))+1,tag_des_size)
##        tag_string = ''
##        for x in tag_des_array:
##            tag_string = tag_string + str(unichr(x))
##        coreDT[-1][1] = tag_string
##        coreDT[-1][3] = str(hex(i+ 12))[2:].zfill(8)
##        if tag_count==1:
##            lastProgTagStartAddr = int(coreDT[-1][0],16)-44  # Last program tag starting address
##        
##        i+=40 # next tag assignment dt

print "Controller tags extracted"
print coreDTheader
for x in coreDT:
    print x
        
print("\n Press any key to continue")
temp=msvcrt.getch()
#######################################################
# SECTION 2 PROGRAM TAGS: 0A dts of different programs can be located at different locations

ctag_size = len(coreDT)

for x in range(0,ctag_size): 
    prog_zone = byteArray_to_LE_string(jlink.memory_read(int(coreDT[x][2],16) -4,4))
##    print prog_zone
    if faddr_program==prog_zone :
        print " \n Found a program with name " + coreDT[x][1]  + ",  Extracting its tags"
        prog_tag_asg_start = byteArray_to_LE_string(jlink.memory_read((int(coreDT[x][2],16)+252),4))# 63*4 added to reach the pointer for tag_allocation_zone for the program
##        print hex(prog_tag_asg_start)
##        prog_tag_asg_start+=252
##        prog_tag_asg_start=hex(prog_tag_asg_start)[2:]
##        print prog_tag_asg_start
        time.sleep(1)

        jlink.close()
        coreDT = fetch_tags(coreDT ,prog_tag_asg_start,coreDT[x][1])
##        time.sleep(1)
        jlink.open(-1)
        jlink.connect('LPC2132')
##i = lastProgTagStartAddr
##while jlink.memory_read(i,4) == tag_alloc_seq:
##    tag_count+=1
##    tag_dt = jlink.memory_read(i,40)
##    coreDT.append([[],[],[],[],[],[],[],[],[]])
##    coreDT[-1][0] = byteArray_to_LE_string(tag_dt[32:36])
##    coreDT[-1][8] = byteArray_to_LE_string(tag_dt[4:8])
##    coreDT[-1][2] = byteArray_to_LE_string(tag_dt[12:16])
##    tag_des_size = jlink.memory_read(int(byteArray_to_LE_int(tag_dt[32:36])),1)[0]
##    tag_des_array = jlink.memory_read(int(byteArray_to_LE_int(tag_dt[32:36]))+1,tag_des_size)
##    tag_string = ''
##    for x in tag_des_array:
##        tag_string = tag_string + str(unichr(x))
##    coreDT[-1][1] = tag_string
##    coreDT[-1][3] = str(hex(i+ 12))[2:].zfill(8)
##    
##    i-=40

##print coreDTheader
##for x in coreDT:
##    print x


###Tag_types
##type_io = 'IO_TAG'
##type_task = 'Task'
##type_prog = 'Program'
##type_routine = 'Routine'
##type_other = 'Others'
###Firmware addresses for various tags types
##faddr_program = '00f58108' # 8000005B
##faddr_routine = '00f5c440' # 80000032
##faddr_tag_asg = '00f55b3c' # 8000000A
##faddr_tag_value= '00f54c54' # 80000007 or 80000008

#####################################################################
# SECTION 3: TAG Type assignment

for x in coreDT:
##    print x[2]
##    print type(x[2])
##    print int(x[2],16)
    fetched_2nd_dword = byteArray_to_LE_string(jlink.memory_read(int(x[2],16)-4,4))
##    print fetched_2nd_dword
    if fetched_2nd_dword == faddr_program:
        x[5] = type_prog
    elif fetched_2nd_dword == faddr_routine:
        x[5] = type_routine
    elif byteArray_to_LE_string(jlink.memory_read(int(x[2],16)-16,4)) == faddr_tag_value: # going back 4dwords to reach firmware addr
        x[5] = type_io
    else:
        x[5] = type_other




#####################################################################
# SECTION: 4  IO_TAG SIZE


for x in coreDT:
    if x[5] == type_io:
        tag_size = (jlink.memory_read(int(x[2],16)-4,1))[0]
        x[6] = str(hex(tag_size))[2:]


print coreDTheader
for x in coreDT:
    print x
    
###################################################################
# SECTION 5 CONTROL LOGIC

# The logic section is organized routine after routine.
# Each routine has a 800000xx start and end marker, with 4th dword of 80000032 pointing at 2nd dword
# Just after the marker, first rung starts
# rung would always start with 7809 '1st half of little endian dword' and rung would end with 7Axxxxxx [where
# xxxxxx represents the last 6 bytes of the address where this data is hosted
# If this is the last rung of routine, it would be followed by '78000000 380D3000 800000xx'

print "\n Extracting the control logic routines"
print("\n Press any key to continue")
temp=msvcrt.getch()

routineDT = []
for x in coreDT:
    if x[5] == type_routine: 
        routineDT.append([  [],[],[],[],[]  ]) # routineName, ProgramName, routine_size, raw
        routineDT[-1][0]=x[1]
        routineDT[-1][1]=x[4]
        
        routine_start_addr = int(hex(byteArray_to_LE_int(jlink.memory_read(int(x[2],16)+4,4))-4)[2:].zfill(8),16)
        time.sleep(0.1)
        routine_size = int(byteArray_to_LE_string(jlink.memory_read(routine_start_addr,4))[2:],16)
        time.sleep(0.1)
        print "Routine " +x[1] + " found at Start address:" + str(routine_start_addr) + " and size ="  + str(routine_size)
        routineDT[-1][2] = str(hex(routine_start_addr)[2:]).zfill(8)
        i= 0
        while i < routine_size:
            routineDT[-1][3].append(byteArray_to_LE_string(jlink.memory_read(routine_start_addr+i*4,4)))
            time.sleep(0.1)
            i+=1
        
for x in routineDT:
    print x
                         

# Raw dwords of the logic area are fetched; Now converting it to actual tags and instructions

for x in routineDT:
    rung_no=-1
    i=1
##    print "len of x[3] = " + str(len(x[3]))

##    while i < len(x[3]):
##        print x[3][i][:4]
##        i+=1
##    i=1
    while i < len(x[3]):
##        print "i = " + str(i)
##        print x[3][i][:4]
        if x[3][i][:4] == '7809':
##            print "Matched 7809 for i =" +str(i)
            rung_no+=1;
##            print "rung no = " + str(rung_no)
            rung_str = "rung "+str(rung_no)
            x[4].append([rung_str])
##            x[4][-1].append(':')
            i+=2 # next dword is skipped
            continue
        elif x[3][i][:2] == '7a': # its rung end; but we are catering for rung end by next rung start seq or by routine end seq
            i+=1
            continue
        elif x[3][i]=='70000000':
            x[4][-1].append('BST') # Branch Start
            i+=1
            continue
        elif x[3][i]=='71000000':
            x[4][-1].append('NXB') # Next Branch 
            i+=1
            continue
        elif x[3][i]=='73000000':
            x[4][-1].append('BND') # Branch End
            i+=1
            continue
        
        elif x[3][i] == '78000000':
##            print "Breaking out of routine as we found x[3][i] = '78000000':: "+ x[3][i]
            break # routine ends
        else: # not 7809..., 7800..., 7809..., or 3rd dword just after 7809..., or 380d3000 (as not reached before break) : All left over are the logic instructions
            bit_number = int(x[3][i][:2],16) % 8
            instr_code = str( hex(int(x[3][i][:2],16) - bit_number))[2:]
            instr_string = INSTR_DICT.get(instr_code, "Unknown")
##            x[4][-1]]+= inst_string
##            x[4][-1][-1]+= ':'

            bit_number = int(x[3][i][0:2],16)%8

            potential_tag = ''
            if x[3][i][2:4] == '08':
                potential_tag='0008' + x[3][i][4:]
##                print potential_tag
            elif x[3][i][2:4] == '80':
                potential_tag = '0c00'+ x[3][i][4:]
            else:
                print "Unknown instruction dword in logic found " + x[3][i]
            
##            print "Searching for this tag " + potential_tag + "  in the coreDT "

            #searching this potential tag in the coreDT
            # convert the tag into 
            byte_number = 0xffff
            tag_string=''
            for y in coreDT:
                delta = int(potential_tag,16)- int(y[2],16)
##                print "calculting " + str(int(potential_tag,16)) +"  -  "+str(int(y[2],16))
##                print 'byte_number = '+ str(byte_number)
                if  delta >= 0 and delta < byte_number:
                    tag_string = copy.copy(y[1])
                    tag_addr = copy.copy(y[2])
                    byte_number = delta
            tag_string = tag_string + '.' +str(byte_number*8 + bit_number)
##            print x[4][-1]
            inst_and_tag = instr_string + "--"+tag_string
            x[4][-1].append(inst_and_tag)

        



        i+=1
print "\n\n Printing coreDT "
for x in coreDT:
    print x
print "\n\n Printing RoutineDT "
for x in routineDT:
    print x

print "\n\n Printing Control Logic "
for x in routineDT:
    for y in x[4]:
        print x[1], x[0],y



###############################################
# Fetching the tag current values

while(1):
    print( "\n \n Press 1 to fetch updated tag values; any other key to terminate.. ")
    user_input=msvcrt.getch()
    print "\n"
    if user_input =='1':
        for x in coreDT:
            b=[]
            if x[5] == type_io:
                a= jlink.memory_read(int(x[2],16),int(x[6],16))
                b.append(x[1])
                for i in a:
                    b.append(str(hex(i))[2:])
                print b
                time.sleep(0.5)
    else: break





   
jlink.close()

###################################
# Writing to file

with open(dest_folder+time_str+'_coreDT.csv','w') as f:
    for item in coreDT:
        print >> f, item

with open(dest_folder+time_str+'_routineDT.csv','w') as f:
    for item in routineDT:
        print >> f, item

        
