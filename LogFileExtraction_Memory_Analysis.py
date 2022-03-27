# Feb 1,2021 Only for log file extraction

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


############################################### Time Zone #################################################
##config_data.append([])
##config_data[-1].append('Time Zone:')
##
##t_z_string_size= byteArray_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[0][1],16),4)) # reading  1st 4 byte fo size of time zone string
##
##
##t_z_array = read_from_dump(list_files, int(CONF_FIELDS[0][1],16)+4, t_z_string_size)
##t_z_string=''
##
##tag_string = ''
##for x in t_z_array:
##    t_z_string = t_z_string + str(unichr(x))
##
##
##config_data[-1].append(t_z_string)
##print config_data
##
############################################### IP ADDRESS #################################################
##
### Look for "Type=\"EN\"" , then look for "Addr=" and then next 12 bytes to contains 3 times "." ; If all match, then fetch from inverted comma to inverted comma after Addr=
##ip_potential_start = int(CONF_FIELDS[1][1],16)
##
##ip_array = read_from_dump(list_files,ip_potential_start,800)
##response_from_strings_fn = strings_in_array(ip_array)
##
##strings_in_ip_array =[]
##
##for x in response_from_strings_fn:
##    strings_in_ip_array.append(x)
## 
##
##ip_index=-1
##ip_str_index=0
##for x in strings_in_ip_array:
##    if x.find("Type=\"EN\" Addr=" )>-1:
##        ip_index= x.find("Type=\"EN\" Addr=")+15
##        if x[ip_index:ip_index+17].count("\"")==2 and x[ip_index:ip_index+16].count(".")==3:
##            ip_start = ip_index + x[ip_index:ip_index+17].find("\"")
##            ip_end = ip_index + x[ip_index:ip_index+17].rfind("\"")
##            break
##
##        else:
##            ip_index=-1
##    ip_str_index+=1
##
##config_data.append([])
##config_data[-1].append('IP Address:')
##
##if ip_index==-1:
##    config_data[1].append("ip address not found")
##
##else:
##    config_data[-1].append(strings_in_ip_array[ip_str_index][ip_start:ip_end+1])
##
##print config_data
##
##
#####################################PROJECT_NAME ####################################################################
##p_name_string =''
##config_data.append([])
##config_data[-1].append('Current Project Name:')
##p_name_size = read_from_dump(list_files,int(CONF_FIELDS[2][1],16),1)[0]
##print type(p_name_size)
##if type(p_name_size) != int:
##    p_name_size = int(p_name_size,16)
##p_name_array = read_from_dump(list_files, int(CONF_FIELDS[2][1],16)+1, p_name_size)
##
##for x in p_name_array:
##    p_name_string = p_name_string + str(unichr(x))
##config_data[-1].append(p_name_string)
##
##print config_data
##
########################################
##
#####################################DEVICE_CATALOG ####################################################################
##catalog_name_string =''
##config_data.append([])
##config_data[-1].append('Device Catalog Name:')
##catalog_name_size = read_from_dump(list_files,int(CONF_FIELDS[3][1],16),1)[0]
##print type(catalog_name_size)
##if type(catalog_name_size) != int:
##    catalog_name_size = int(p_name_size,16)
##catalog_name_array = read_from_dump(list_files, int(CONF_FIELDS[3][1],16)+1, catalog_name_size)
##
##for x in catalog_name_array:
##    catalog_name_string = catalog_name_string + str(unichr(x))
##
##config_data[-1].append(catalog_name_string)
##
##print config_data
##
########################################
##
##################################### REVISION NO ####################################################################
##revision_string =''
##config_data.append([])
##config_data[-1].append('Revision No:')
##
##rev_array = read_from_dump(list_files,int(CONF_FIELDS[4][1],16),40)
##response_from_strings_fn = strings_in_array(rev_array)
##
##for x in response_from_strings_fn:
##   revision_string = x
##   break # interested in the 1st string only
##
##
##config_data[-1].append(revision_string)
##
##print config_data
##
########################################
##
##
##
##################################### SD CARD FILES ####################################################################
##sd_filenames =[]
##sd_strings=[]
##config_data.append([])
##config_data[-1].append('SD Card Files: ')
##
##sd_array = read_from_dump(list_files,int(CONF_FIELDS[7][1],16),int(CONF_FIELDS[7][2],16))
##response_from_strings_fn = strings_in_array(sd_array)
##
##for x in response_from_strings_fn:
##   sd_strings.append(x)
##
##for x in sd_strings:
##    if x == "USER_INITIATED":
##        load_image = "USER_INITIATED"
##    elif x== "ON_POWER_ON":
##        load_image = " ON_POWER_ON"
##    elif x == "ON_CORRUPT_MEMORY":
##        load_image ="ON_CORRUPT_MEMORY"
##
##    if x == "PROGRAM":
##        load_mode="PROGRAM"
##    elif x=="RUN":
##        load_mode = "RUN"
##
##    if x.find("p5k")>1:
##        sd_config_file=x
##    elif x.find("bin")>1:
##        sd_firmware=x
##
##config_data[-1].append(sd_config_file)
##config_data[-1].append(sd_firmware)
##
##config_data.append([])
##config_data[-1].append('SD_Load_Mode')
##config_data[-1].append(load_mode)
##
##config_data.append([])
##config_data[-1].append('SD_Load_Image')
##config_data[-1].append(load_image)   
##
##
##
##
########################################
##
##
##
##################################### TIME SINCE RESTART ####################################################################
##
##config_data.append([])
##config_data[-1].append('Time since PLC restart: ')
##
##time_since_restart = sixBytes_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[10][1],16),6))
##response_from_strings_fn = strings_in_array(sd_array)
##
##
##
##
##config_data[-1].append(time_since_restart)
##
##
########################################
##
##
##
##
##################################### DESKTOP NAME ####################################################################
##
##config_data.append([])
##config_data[-1].append('Desktop Name: ')
##desktop_name = ""
##
##desktop_name_size = 2 * (twoBytes_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[11][1],16),2))) # multiplied by 2 as the size is in words
##print str(desktop_name_size )+ " is desktop_name_size"
##desktop_name_array = read_from_dump(list_files,int(CONF_FIELDS[11][1],16)+2,desktop_name_size) # +2 to skip the size word
##
##i2=0
##while (i2 < desktop_name_size):
##    desktop_name = desktop_name + str(unichr(desktop_name_array[i2]))
##    i2+=2
##
##config_data[-1].append(desktop_name)
##
########################################
##with open(dest_folder+time_str+'_configData.csv','w') as f:  # saving in the configData file
##    for item in config_data:
##        print >> f, item
##
##
##################################### XML FILE ####################################################################
##xml_f_content =''
##config_data.append([])
##config_data[-1].append('xml file')
##j=0
##x = read_from_dump(list_files,int(CONF_FIELDS[5][1],16),1)
##print x
##
##while x[0] != 255: # FF
##    xml_f_content =xml_f_content + str(unichr(x[0]))
##    j+=1
##    x = read_from_dump(list_files,int(CONF_FIELDS[5][1],16)+j,1)
##
### confirmation check
##x = byteArray_to_LE_int(read_from_dump(list_files,int(CONF_FIELDS[6][1],16),4))
##if (x > len(xml_f_content) and x-len(xml_f_content) <4) or (x <= len(xml_f_content) and len(xml_f_content) - x <4):
##   config_data[-1].append("Confidence HIGH")
##else:
##    config_data[-1].append("Confidence LOW")
##                                                           
##config_data[-1].append([xml_f_content])
##
##
##f= open(dest_folder+time_str+'_xml_file.xml','ab') # saving xml file separately
##for i in config_data[-1][-1][0]:
##    f.write(i)
##f.close()
##
##with open(dest_folder+time_str+'_configData.csv','a') as f:  # updaing complete configData file
##    print >> f, config_data[-1][-1][0]

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


f= open(dest_folder+time_str+'_log_file.txt','a') # saving log file separately
for i in config_data[-1]:
    print >> f, i

f.close()

for x in config_data:
    print x



exit() ################################################*********************************************


######################################
#######################################









