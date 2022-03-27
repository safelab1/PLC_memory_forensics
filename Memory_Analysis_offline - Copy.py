# Jan 14,2020 : This is memory_analysis module for Allen Bradley ControlLogic 1756
# Jan 14,2020: As of the date, it can handle projects with multiple programs with multiple routines with multiple rungs with multiple instructions. So far we incorporated common instructions only
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
import time
import msvcrt
import os
import os.path
from os import listdir
from os.path import isfile, join
from Read_from_dump import *

from Little_endian_conversions import *
from Tags_fetcher_offline import *
from Instr_dictionary import *
from Extract_strings import *



time_str = time.strftime("%Y%m%d-%H%M%S")
dump_folder = input("Enter the memory dumps folder path: ")
memFiles = [f for f in listdir(dump_folder) if isfile(join(dump_folder, f))] # only files excl folders
dest_folder = dump_folder + "/analysis"
proj_files = dump_folder + "/project_files"
if not os.path.isdir(proj_files):  # For saving project acd file / snapshots etc
    os.mkdir(proj_files)

if not os.path.isdir(dest_folder):  # checking if analysis carried out previously, and folder exists
    os.mkdir(dest_folder)
dest_folder = dest_folder + '/'+time_str+'/' # updating dest_folder to preserve all previous analyses
os.mkdir(dest_folder)

list_files = []
for x in memFiles:
    name_parts = x.split('_')
    list_files.append(name_parts) # list_files[0] is start_add , list_files[1] is end_addr
    list_files[-1].insert(0,x)
for x in list_files:  # converting to int
    print x
    x[1] = int(x[1],16)
    x[2] = int (x[2],16)
    f_to_open = dump_folder + x[0]

    ff = open(f_to_open,'rb')
    temp = ff.read()
    temp2 = bytearray(temp)
    x[3] =[]
    for i in temp2:
        x[3].append(bytes(i))
        x[3][-1] = int(x[3][-1])



addr_cTag_asg_zone = '0027FE3C'
addr_ControlLogic_end = '0027FE5C'






########################################################################################################3
# SECTION:6 OTHER CONFIGURATION DATA
config_data =[]

CONF_FIELDS = [
    ['time_zone_addr' , '00023c10' ], # 1st dword is size, then ascii follows
    ['ip_address_locality' ,'00080000'], # fetch via string and search in region
    ['proj_name' , '00024000'] , # 1st byte is size, then ascii for current project in plc
    ['device_catalog' , '000241c4'], # 1st byte is size, then ascii
    ['revision' , '000241f0'],  # fetch till ascii found; confidence LOW
    ['xml_file_addr' , '0004b1e0'] ,  # file would terminate when stream of FFFFFF starts; confidence LOW
    ['xml_file_size_location' , '0004b1b0'], # the size of xml file is mentioned here L.Endian dword; confidence LOW
   [ 'SD_card_files' ,'00024400','300'], # Fetch 0x300 bytes; run string to find filenames by searching(file1)".p5k"  (2) "Executive.bin"
   [ 'load_image' , '00024438'], # SD card related setting
    ['load_mode'  , ' 00024460'], # SD card related setting
    ['time_since_restart' , '0027A9D2'], #6 bytes in little endian format (provides ms)
    ['desktop_name' , '0004C044'], # 1st word (16 bytes LEndian) is number of words; next UTF-16 format letters
    ['controller_log','00880000'] # 6th dword = no of loads/mode changes ; contl_name allow abc ABC.. 123.. _ ie 48 to 90, 95; 13th dword is 1st record#->from recNo, 7thdword=name if contr change; if mode change then 1xx or 2xx or 3xx
]


############################################# Time Zone #################################################
config_data.append([])
config_data[-1].append('Time Zone:')

t_z_string_size= byteArray_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[0][1],16),4)) # reading  1st 4 byte fo size of time zone string


t_z_array = read_from_dump(list_files, int(CONF_FIELDS[0][1],16)+4, t_z_string_size)
t_z_string=''

tag_string = ''
for x in t_z_array:
    t_z_string = t_z_string + str(unichr(x))


config_data[-1].append(t_z_string)
print config_data

############################################# IP ADDRESS #################################################

# Look for "Type=\"EN\"" , then look for "Addr=" and then next 12 bytes to contains 3 times "." ; If all match, then fetch from inverted comma to inverted comma after Addr=
ip_potential_start = int(CONF_FIELDS[1][1],16)

ip_array = read_from_dump(list_files,ip_potential_start,800)
response_from_strings_fn = strings_in_array(ip_array)

strings_in_ip_array =[]

for x in response_from_strings_fn:
    strings_in_ip_array.append(x)
 

ip_index=-1
ip_str_index=0
for x in strings_in_ip_array:
    if x.find("Type=\"EN\" Addr=" )>-1:
        ip_index= x.find("Type=\"EN\" Addr=")+15
        if x[ip_index:ip_index+17].count("\"")==2 and x[ip_index:ip_index+16].count(".")==3:
            ip_start = ip_index + x[ip_index:ip_index+17].find("\"")
            ip_end = ip_index + x[ip_index:ip_index+17].rfind("\"")
            break

        else:
            ip_index=-1
    ip_str_index+=1

config_data.append([])
config_data[-1].append('IP Address:')

if ip_index==-1:
    config_data[1].append("ip address not found")

else:
    config_data[-1].append(strings_in_ip_array[ip_str_index][ip_start:ip_end+1])

print config_data


###################################PROJECT_NAME ####################################################################
p_name_string =''
config_data.append([])
config_data[-1].append('Current Project Name:')
p_name_size = read_from_dump(list_files,int(CONF_FIELDS[2][1],16),1)[0]
print type(p_name_size)
if type(p_name_size) != int:
    p_name_size = int(p_name_size,16)
p_name_array = read_from_dump(list_files, int(CONF_FIELDS[2][1],16)+1, p_name_size)

for x in p_name_array:
    p_name_string = p_name_string + str(unichr(x))
config_data[-1].append(p_name_string)

print config_data

######################################

###################################DEVICE_CATALOG ####################################################################
catalog_name_string =''
config_data.append([])
config_data[-1].append('Device Catalog Name:')
catalog_name_size = read_from_dump(list_files,int(CONF_FIELDS[3][1],16),1)[0]
print type(catalog_name_size)
if type(catalog_name_size) != int:
    catalog_name_size = int(p_name_size,16)
catalog_name_array = read_from_dump(list_files, int(CONF_FIELDS[3][1],16)+1, catalog_name_size)

for x in catalog_name_array:
    catalog_name_string = catalog_name_string + str(unichr(x))

config_data[-1].append(catalog_name_string)

print config_data

######################################

################################### REVISION NO ####################################################################
revision_string =''
config_data.append([])
config_data[-1].append('Revision No:')

rev_array = read_from_dump(list_files,int(CONF_FIELDS[4][1],16),40)
response_from_strings_fn = strings_in_array(rev_array)

for x in response_from_strings_fn:
   revision_string = x
   break # interested in the 1st string only


config_data[-1].append(revision_string)

print config_data

######################################



################################### SD CARD FILES ####################################################################
sd_filenames =[]
sd_strings=[]
config_data.append([])
config_data[-1].append('SD Card Files: ')

sd_array = read_from_dump(list_files,int(CONF_FIELDS[7][1],16),int(CONF_FIELDS[7][2],16))
response_from_strings_fn = strings_in_array(sd_array)

for x in response_from_strings_fn:
   sd_strings.append(x)

for x in sd_strings:
    if x == "USER_INITIATED":
        load_image = "USER_INITIATED"
    elif x== "ON_POWER_ON":
        load_image = " ON_POWER_ON"
    elif x == "ON_CORRUPT_MEMORY":
        load_image ="ON_CORRUPT_MEMORY"

    if x == "PROGRAM":
        load_mode="PROGRAM"
    elif x=="RUN":
        load_mode = "RUN"

    if x.find("p5k")>1:
        sd_config_file=x
    elif x.find("bin")>1:
        sd_firmware=x

config_data[-1].append(sd_config_file)
config_data[-1].append(sd_firmware)

config_data.append([])
config_data[-1].append('SD_Load_Mode')
config_data[-1].append(load_mode)

config_data.append([])
config_data[-1].append('SD_Load_Image')
config_data[-1].append(load_image)   




######################################



################################### TIME SINCE RESTART ####################################################################

config_data.append([])
config_data[-1].append('Time since PLC restart: ')

time_since_restart = sixBytes_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[10][1],16),6))
response_from_strings_fn = strings_in_array(sd_array)




config_data[-1].append(time_since_restart)


######################################




################################### DESKTOP NAME ####################################################################

config_data.append([])
config_data[-1].append('Desktop Name: ')
desktop_name = ""

desktop_name_size = 2 * (twoBytes_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[11][1],16),2))) # multiplied by 2 as the size is in words
print str(desktop_name_size )+ " is desktop_name_size"
desktop_name_array = read_from_dump(list_files,int(CONF_FIELDS[11][1],16)+2,desktop_name_size) # +2 to skip the size word

i2=0
while (i2 < desktop_name_size):
    desktop_name = desktop_name + str(unichr(desktop_name_array[i2]))
    i2+=2

config_data[-1].append(desktop_name)

######################################
with open(dest_folder+time_str+'_configData.csv','w') as f:  # saving in the configData file
    for item in config_data:
        print >> f, item


################################### XML FILE ####################################################################
xml_f_content =''
config_data.append([])
config_data[-1].append('xml file')
j=0
x = read_from_dump(list_files,int(CONF_FIELDS[5][1],16),1)
print x

while x[0] != 255: # FF
    xml_f_content =xml_f_content + str(unichr(x[0]))
    j+=1
    x = read_from_dump(list_files,int(CONF_FIELDS[5][1],16)+j,1)

# confirmation check
x = byteArray_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[6][1],16),4))
if (x > len(xml_f_content) and x-len(xml_f_content) <4) or (x <= len(xml_f_content) and len(xml_f_content) - x <4):
   config_data[-1].append("Confidence HIGH")
else:
    config_data[-1].append("Confidence LOW")
                                                           
config_data[-1].append([xml_f_content])


f= open(dest_folder+time_str+'_xml_file.xml','ab') # saving xml file separately
for i in config_data[-1][-1][0]:
    f.write(i)
f.close()

with open(dest_folder+time_str+'_configData.csv','a') as f:  # updaing complete configData file
    print >> f, config_data[-1][-1][0]

######################################
################################### CONTROLLER / MODE LOGS ####################################################################

config_data.append([])
config_data[-1].append('ControllerLog: ')
number_of_logs=0
log_start_addr = int(CONF_FIELDS[12][1],16)
print read_from_dump(list_files,(int(CONF_FIELDS[12][1],16)),28)
count_of_logs = fourBytes_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[12][1],16)+6*4,4))
print "Total no of logs " +  str(count_of_logs )
mode=''
new_log_addr = log_start_addr + 12*4 # first log starts at 00800030;#  then after every 364 bytes
for i in range(0,count_of_logs):
    log_number = i+1
    
##    print hex(new_log_addr)
##    print fourBytes_to_LE_int(read_from_dump(list_files,new_log_addr,4))
    
    if fourBytes_to_LE_int(read_from_dump(list_files,new_log_addr,4))==log_number:
##        print "Log number matches for log " +str(log_number)
        config_data[-1].append([])
        config_data[-1][-1].append(log_number)
        mode_or_name_start = fourBytes_to_LE_int(read_from_dump(list_files,new_log_addr + 28,4))
##        print hex(mode_or_name_start)
        if mode_or_name_start < 1280: # < 500, means not a project name; and only mode change # another check could be for string
            if mode_or_name_start >=0x100 and mode_or_name_start < 0x200:
                mode = "PROG"
            elif mode_or_name_start >=0x200 and mode_or_name_start<0x300:
                mode = "RUN"
            elif mode_or_name_start >=0x300 and mode_or_name_start < 0x400:
                mode = "TEST"
            else:
                mode = "UNKNOWN"
            config_data[-1][-1].append("PLC mode change event: New mode is " + mode)
        else:
            j=0
            new_name=""
##            print read_from_dump(list_files,new_log_addr + 28 + j,1)[0]
            new_ch_for_name = read_from_dump(list_files,new_log_addr + 28 + j,1)[0]
            while (new_ch_for_name >=48 and new_ch_for_name <=57) or (new_ch_for_name >=65 and new_ch_for_name <=90)  or (new_ch_for_name >=95 and new_ch_for_name <=122) :
                new_name = new_name + str(unichr(new_ch_for_name))
                j+=1
                new_ch_for_name = read_from_dump(list_files,new_log_addr + 28 + j,1)[0]
            config_data[-1][-1].append("Project Download Event : Controller Name is " + new_name)

    new_log_addr = new_log_addr +364
                
##time.sleep(50)
for x in config_data:
    print x
    
with open(dest_folder+time_str+'_configData.csv','a') as f:  # updaing complete configData file
    print >> f, config_data[-1]

f= open(dest_folder+time_str+'_log_file.txt','a') # saving log file separately
for i in config_data[-1]:
    print >> f, i

f.close()

for x in config_data:
    print x



################################################*********************************************


######################################
#######################################








##########

coreDT = []
print read_from_dump(list_files,addr_cTag_asg_zone,4)
control_tag_start = byteArray_to_LE_string(read_from_dump(list_files,addr_cTag_asg_zone,4))
print control_tag_start
print "Control tag start above"
print hex(int(control_tag_start,16))
if control_tag_start == '00000000':
    print "No control logic found in the dump through list walking"
    exit()
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

print "Going for fetch_tags_offline"
coreDT = fetch_tags_offline(list_files,coreDT,control_tag_start,"controller")


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
        
##print("\n Press any key to continue")
##temp=msvcrt.getch()
#######################################################
# SECTION 2 PROGRAM TAGS: 0A dts of different programs can be located at different locations

ctag_size = len(coreDT)

print "prog_zone=----------------------------------------------------------------------------------"

for x in range(0,ctag_size): 
    prog_zone = read_from_dump(list_files,int(coreDT[x][2],16) -4,4)
    if prog_zone == -1:
        print "Tag not found due to unavailability of required mem address " + coreDT[x][2] + " in the dump "
        continue
    else:
        prog_zone = byteArray_to_LE_string(prog_zone)
##    print prog_zone
##    print type(prog_zone)
##    print faddr_program
    if faddr_program==prog_zone :
        print " \n Found a program with name " + coreDT[x][1]  + ",  Extracting its tags"
        prog_tag_asg_start = (read_from_dump(list_files,(int(coreDT[x][2],16)+252),4))# 63*4 added to reach the pointer for tag_allocation_zone for the program
        if prog_tag_asg_start==-1:
            print "Tag not found due to unavailability of required mem address " + str(hex(int(coreDT[x][2],16)+252))[2:] + " in the dump "
            continue
        else:
            prog_tag_asg_start = byteArray_to_LE_string(prog_tag_asg_start)
        print prog_tag_asg_start

 
        coreDT = fetch_tags_offline(list_files, coreDT ,prog_tag_asg_start,coreDT[x][1])

##        time.sleep(1)


print coreDTheader
for x in coreDT:
    print x


##
#######################################################################
### SECTION 3: TAG Type assignment
##
for x in coreDT:
##    print x[2]
##    print type(x[2])
##    print int(x[2],16)
    fetched_2nd_dword = (read_from_dump(list_files,int(x[2],16)-4,4))
##    print "Fetched_2nd_dword ="
##    print fetched_2nd_dword
    if fetched_2nd_dword == -1:
        continue
    else:
        fetched_2nd_dword = byteArray_to_LE_string(fetched_2nd_dword)
        
##    print fetched_2nd_dword
    if fetched_2nd_dword == faddr_program:
        x[5] = type_prog
    elif fetched_2nd_dword == faddr_routine:
        x[5] = type_routine
    elif byteArray_to_LE_string(read_from_dump(list_files,int(x[2],16)-16,4)) == faddr_tag_value: # going back 4dwords to reach firmware addr
        x[5] = type_io
    else:
        x[5] = type_other




#######################################################################
### SECTION: 4  IO_TAG SIZE
##
##
for x in coreDT:
    if x[5] == type_io:
        tag_size = (read_from_dump(list_files,int(x[2],16)-4,1))[0]
        x[6] = str(hex(tag_size))[2:]


print coreDTheader
for x in coreDT:
    print x
    
#####################################################################
# SECTION 5 CONTROL LOGIC

# The logic section is organized routine after routine.
# Each routine has a 800000xx start and end marker, with 4th dword of 80000032 pointing at 2nd dword
# Just after the marker, first rung starts
# rung would always start with 7809 '1st half of little endian dword' and rung would end with 7Axxxxxx [where
# xxxxxx represents the last 6 bytes of the address where this data is hosted
# If this is the last rung of routine, it would be followed by '78000000 380D3000 800000xx'

print "\n Extracting the control logic routines"
##print("\n Press any key to continue")
##temp=msvcrt.getch()

routineDT = []
for x in coreDT:
    if x[5] == type_routine: 
        routineDT.append([  [],[],[],[],[]  ]) # routineName, ProgramName, routine_size, raw
        routineDT[-1][0]=x[1]
        routineDT[-1][1]=x[4]
        
        routine_start_addr = int(hex(byteArray_to_LE_int(read_from_dump(list_files,int(x[2],16)+4,4))-4)[2:].zfill(8),16)
        time.sleep(0.1)
        routine_size = int(byteArray_to_LE_string(read_from_dump(list_files,routine_start_addr,4))[2:],16)
        time.sleep(0.1)
        print "Routine " +x[1] + " found at Start address:" + str(routine_start_addr) + " and size ="  + str(routine_size)
        routineDT[-1][2] = str(hex(routine_start_addr)[2:]).zfill(8)
        i= 0
        while i < routine_size:
            routineDT[-1][3].append(byteArray_to_LE_string(read_from_dump(list_files,routine_start_addr+i*4,4)))
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
##        print x[3][i]
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
            x[4][-1].append("BST") # Branch Start
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
        elif x[3][i][:3]== '004':   # One-shot Instructions  addedd on Feb 18,2020........................................
            instr_size= int(x[3][i][4],16)+7  # dwords count
            instr_code = x[3][i][4:]
            instr_string = INSTR_DICT.get(instr_coode,"Unknnown")

            if instr_code == '8012': #...................>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONS
                if x[3][i+4][:2] != '8e':
                    instr_string = "UNKNOWN"
                    i+=instr_size
                    continue
                else:
                    bit_number = int(x[3][i+j][6:],16)
                    if x[3][i+6][:2] == '8f': # it means a physical tag is being used 
                        potential_tag = '0c00'+ x[3][i+5][4:]
                    else:
                        potential_tag = str(int(x[3][i+5][2:],16))[2:].zfill(8)
                    bit_number = int(x[3][i+4][4:],16)
                    for y in coreDT:
                        if potential_tag == y[2]:
                            tag_string = copy.copy(y[1]) + "." + str(bit_number)
                            inst_and_tag = instr_string + "--"+tag_string
                            x[4][-1].append(inst_and_tag)
                            break
                    i+=instr_size
                    continue
                
            elif instr_code == '8013': #.>>>>>>>>>>>>>>>>>>>>>>>>>>>> OSR: contains 2 x tags: 1st for storageBit; other for outputBit 
                if x[3][i+4][:2] != '8e':
                    instr_string = "UNKNOWN"
                    i=i+instr_size
                    continue
                else:
                    bit_number = int(x[3][i+j][6:],16)
                    if x[3][i+6][:2] == '8f': # it means a physical tag is being used for storageBit
                        potential_tag = '0c00'+ x[3][i+5][4:]
                        first_tag_size = 3
                    else:
                        potential_tag = str(int(x[3][i+5][2:],16))[2:].zfill(8)
                        first_tag_size = 2

                    for y in coreDT:
                        if potential_tag == y[2]:
                            tag_string = copy.copy(y[1])
                            inst_and_tag = instr_string + "--"+"storageBit="+tag_string
                            x[4][-1].append(inst_and_tag)
                            break
                    # now finding outputBit
                    bit_number = int(x[3][i+j+first_tag_size][6:],16)
                    if x[3][i+6+first_tag_size][:2] == '8f': # it means a physical tag is being used for storageBit
                        potential_tag = '0c00'+ x[3][i+5+first_tag_size][4:]
                        
                    else:
                        potential_tag = str(int(x[3][i+5+first_tag_size][2:],16))[2:].zfill(8)
                        

                    for y in coreDT:
                        if potential_tag == y[2]:
                            tag_string = copy.copy(y[1])
                            inst_and_tag = inst_and_tag + "--"+"outputBit="+tag_string
                            x[4][-1].append(inst_and_tag)
                            break
                    i+=instr_size
                    continue

            elif instr_code == '8014': #.>>>>>>>>>>>>>>>>>>>>>>>>>>>> OSF: contains 2 x tags: 1st for storageBit; other for outputBit 
                if x[3][i+4][:2] != '8e':
                    instr_string = "UNKNOWN"
                    i=i+instr_size
                    continue
                else:
                    bit_number = int(x[3][i+j][6:],16)
                    if x[3][i+6][:2] == '8f': # it means a physical tag is being used for storageBit
                        potential_tag = '0c00'+ x[3][i+5][4:]
                        first_tag_size = 3
                    else:
                        potential_tag = str(int(x[3][i+5][2:],16))[2:].zfill(8)
                        first_tag_size = 2

                    for y in coreDT:
                        if potential_tag == y[2]:
                            tag_string = copy.copy(y[1])
                            inst_and_tag = instr_string + "--"+"storageBit="+tag_string
                            x[4][-1].append(inst_and_tag)
                            break
                    # now finding outputBit
                    bit_number = int(x[3][i+j+first_tag_size][6:],16)
                    if x[3][i+6+first_tag_size][:2] == '8f': # it means a physical tag is being used for storageBit
                        potential_tag = '0c00'+ x[3][i+5+first_tag_size][4:]
                        
                    else:
                        potential_tag = str(int(x[3][i+5+first_tag_size][2:],16))[2:].zfill(8)
                        

                    for y in coreDT:
                        if potential_tag == y[2]:
                            tag_string = copy.copy(y[1])
                            inst_and_tag = inst_and_tag + "--"+"outputBit="+tag_string
                            x[4][-1].append(inst_and_tag)
                            break
                    i+=instr_size
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
##            print x[4]
            inst_and_tag = instr_string + "--"+tag_string
            x[4][-1].append(inst_and_tag)

    

        i+=1

#################################################
# Fetching the tag values

for x in coreDT:
    b=[]
    if x[5] == type_io:
        a= read_from_dump(list_files,int(x[2],16),int(x[6],16))
        for i in a:
            b.append(str(hex(i))[2:])
        x[7] = b



print "\n\n\nAfter fetching the tag values from the memory dump"
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





# Time since last reboot



##config_data[0].append(list_files, config_data[0])









##
#####################################
# Writing to file

with open(dest_folder+time_str+'_coreDT.csv','w') as f:
    for item in coreDT:
        print >> f, item

with open(dest_folder+time_str+'_routineDT.csv','w') as f:
    for item in routineDT:
        print >> f, item


with open(dest_folder+time_str+'_config_data.csv','w') as f:
    for item in routineDT:
        print >> f, item

        
######################################################


