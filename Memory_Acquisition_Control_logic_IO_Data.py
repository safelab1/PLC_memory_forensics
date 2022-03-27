# Main program to fetch selected content of the 1756 memory via JTAG segger debugger using pylink library.
# This program only fetches part of the memory that contains control logic and IO Data
# For control logic, both parts encapsulated by 80000001 are captured. But for IO Data, only 1st part is picked
# The second part of IO Data region is very sensitive to be picked and need to be acquired very slowly. Moreover, concerned IO tags are in part-1


import pylink
import time
import os

from Marker_based_acquisition import *

default_wait = 4 # second
default_block = 8192

timestr = time.strftime("%Y%m%d-%H%M%S")
addr_ranges = [ [ '00080000', '0027fFFF' , 2048 , 0 , 4 , '80000001' ] ,
                [ '0C004000', '0C07F7FF' , 4 , 0 , 4, '80000001' ]]

if not os.path.isdir('./data'): # all mem_acquisitions are saved in ./data
    os.mkdir('./data')

dest_folder="./data/"+timestr
os.mkdir(dest_folder)

p_folder=dest_folder +"/" +"project_files"
os.mkdir(p_folder)

analysis_folder=dest_folder +"/" +"analysis"
os.mkdir(analysis_folder)

for x in addr_ranges:
    if x[4] !=0:
        wait_time = x[4]
    else:
       wait_time = default_wait
    if x[2] != 0:
        blocksize = x[2]
    else:
        blocksize = default_block

    if x[5] == 0: # non-marker based acquisition
        
        f= open(dest_folder+"/"+ x[0]+"_"+ x[1]+"_"+timestr+ ".bin",'ab')
        jlink = pylink.JLink()
        jlink.open(-1)
        jlink.connect('LPC2132')
        
        start_addr = int(x[0],16)
        end_addr = int(x[1],16)
        i= start_addr
        while(i < end_addr):
            if (end_addr - i) > blocksize:
                a = jlink.memory_read(i,blocksize)
                b = bytearray(a)
               # print b[0],b[1],b[2],b[3]
                f.write(b)
                i+=blocksize
            else:
                a = jlink.memory_read(i,end_addr -i+1)
                i = end_addr
                b = bytearray(a)
                f.write(b)
            time.sleep(wait_time)

        jlink.close()
        f.close()

            
    else:
        print "NOT ZERO MARKER" + str(x[5])
        if addr_ranges.index(x)==0:
            mb_acquisition_conLogic(x,dest_folder,timestr)
        else:
            time.sleep(4)
            mb_acquisition_upper_part_only(x,dest_folder,timestr)


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

    

