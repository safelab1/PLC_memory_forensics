# Main program to fetch the 1756 memory via JTAG segger debugger using pylink library
# The program fetches the address_ranges from other file, and acquires data as per the chunksize, wait time, speed and markers settings described in the Address_Ranges.py
# The program creates a directory with the curent_time as the name, and saves all mem files in that folder
# The mem file addressing is done as per following convention
# "startAddrInHex_endAddrInHex_time.bin ". The convention helps memory analysis module to calculate offsets


import pylink
import time
import os
from Address_Ranges import addr_ranges # source of address ranges to be acquired
from Marker_based_acquisition import mb_acquisition 
from Acquisition_functions import *


default_wait = 1 # second
default_block = 8192

timestr = time.strftime("%Y%m%d-%H%M%S")

if not os.path.isdir('./data'): # all mem_acquisitions are saved in ./data
    os.mkdir('./data')

dest_folder="./data/"+timestr
os.mkdir(dest_folder)

p_folder=dest_folder +"/" +"project_files"
os.mkdir(p_folder)

analysis_folder=dest_folder +"/" +"analysis"
os.mkdir(analysis_folder)

response_time=[]



print("Welcome to the Memory Acquisition via JTAG ")
print("Select required option from the menu")

opt1=-1
while (opt1 !=1 and opt1 !=2 and opt1!=3):
    print ("1: To acquire complete list of address blocks")
    print ("2: To acquire one specific block")
    print ("3: To acquire customized address range")
    opt1 = input(" Please enter the choice from above: ")

if opt1==1:
    acquire_complete_memory();
    print "1"
elif opt1==2:
    i=0
    for x in addr_ranges:
        print str(addr_ranges.index(x))+ " " +str(x)
        i+=1
        opt2=-1
    while opt2<1 or opt2 >i:
        opt2 = input("Please enter the serial no of the desired mem block or enter -1 to exit: ")
        if opt2==-1:
            exit()
        else:
            acquire_specific_range(dest_folder, timestr, addr_ranges[opt2][0],addr_ranges[opt2][1],addr_ranges[opt2][2],addr_ranges[opt2][3],addr_ranges[opt2][4],addr_ranges[opt2][5]);

elif opt1==3:
    st_status=0
    while(st_status!=1):
        starting_add = input("Please enter starting address in hex format with inverted comma as '12ab4500'  : ")
        try:
            int(starting_add,16)
            st_status =1;
        except:
            print ("Incorrect input: use format with inverted comma as '12ab4500'  : ")
        
    end_status=0
    while(end_status!=1):
        end_add = input("Please enter starting address in hex format with inverted comma as '12ab4500'  : ")
        try:
            int(end_add,16)
            end_status =1;
        except:
            print ("Incorrect input: use format with inverted comma as '12ab4500'  : ")

    chunk_size = input(" Enter blocksize in no of bytes: Enter 0 for default 8192 :")
    if chunk_size == 0:
        chunk_size = default_block

    debugger_speed=0 
##    debugger_speed = input(" Enter debugger connection speed: Enter 0 for default 8192 :")
##    if chunk_size == 0:
##        chunk_size = default_block
    
       
    wait_time = input(" Enter wait time between reads in seconds: Enter 0 or 1 for default 1 sec :")
    if wait_time == 0 or wait_time ==1 :
        wait_time = default_wait

    
    
    acquire_specific_range(starting_add, end_addr,chunk_size, debugger_speed, wait_time, 0) # last zero is for non marker based acquisition

        

##
##

##jlink.AUTO_JTAG_SPEED=0  # For adapting speed
#jlink.MAX_JTAG_SPEED = 4000

#starting_address = 0x50270000  #enter starting hex address
#ending_address = 0x5027ffff  # enter ending hex address

##starting_address = 0x027a8e0
##ending_address = 0x0027ffff
##chunk_size = 8196
##sleep_duration = 4
##
##
##start_decimal = int(starting_address)
##end_decimal = int(ending_address)
##print (end_decimal - start_decimal )
##testfile = open(dest_folder+"_"+tag_number+"_v_" +tag_value+" _time_"+str(timestr) + "_mem_from_"+hex(starting_address)+"_to_"+hex(ending_address)+".bin","ab")
##x= start_decimal
##while(x < end_decimal):
##    if (end_decimal - x) > chunk_size:
##        a = jlink.memory_read(x,chunk_size)
##        b = bytearray(a)
##       # print b[0],b[1],b[2],b[3]
##        testfile.write(b)
##        x = x + chunk_size
##    else:
##        a = jlink.memory_read(x,end_decimal - x+1)
##        x = end_decimal
##        b = bytearray(a)
##        testfile.write(b)
##    time.sleep(sleep_duration)
##testfile.close()

    

