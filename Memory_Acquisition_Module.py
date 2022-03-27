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

default_wait = 0.1 # second
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
for x in addr_ranges:
    print "New range being fetched: from " + x[0] + " to " + x[1] + "Starting at Time : " +str(time.strftime("%Y%m%d-%H%M%S"))
    
    if x[4] !=0:
        wait_time = x[4]
    else:
       wait_time = default_wait
    if x[2] != 0:
        blocksize = x[2]
    else:
        blocksize = default_block

    if x[5] == 0: # non-marker based acquisition

##        wait_time = 1  #############################################################TESTING ONLY
##        blocksize = 8192 ############################################################TESTING ONLY
        
        jlink = pylink.JLink()
        jlink.open(-1)
        jlink.MAX_BUF_SIZE=500000
        jlink.connect('LPC2880')
        start_addr = int(x[0],16)
        end_addr = int(x[1],16)
        i= start_addr
        count=0
        no_of_count_before_writing = 10
        while(i < end_addr):
            
            count+=1
            if count % no_of_count_before_writing ==0:
                jlink.close()       ########################### Trial on Jan 20, for handling the problem of plc disconnection from engg
                print hex(i)[2:].zfill(8)
                f1=open(dest_folder+"/"+ x[0]+"_"+ x[1]+"_response_time_list_"+timestr+".csv",'a')
                while len(response_time) >0:
                    y = response_time.pop()
                    for j in y:
                        f1.write(str(j))
                        f1.write(",")
                    f1.write("\n")
                f1.close()
                time.sleep(3)
                jlink = pylink.JLink()
                jlink.open(-1)
                jlink.MAX_BUF_SIZE=500000
                jlink.connect('LPC2880')
                
                
            response_time.append([]) 
            if (end_addr - i) > blocksize:
                time1 = time.time()
                a = jlink.memory_read(i,blocksize)
                time2 = time.time()
                response_time[-1].append(hex(i)[2:].zfill(8))
                response_time[-1].append(time2-time1)
                print response_time[-1]
                b = bytearray(a)
               # print b[0],b[1],b[2],b[3]
                f= open(dest_folder+"/"+ x[0]+"_"+ x[1]+"_"+timestr+ ".bin",'ab')
                f.write(b)
                f.close()
                i+=blocksize
            else:
                a = jlink.memory_read(i,end_addr -i+1)
                i = end_addr
                b = bytearray(a)
                f= open(dest_folder+"/"+ x[0]+"_"+ x[1]+"_"+timestr+ ".bin",'ab')
                f.write(b)
                f.close()
            time.sleep(wait_time)

        jlink.close()

            
    else:
        print "NOT ZERO MARKER" + str(x[5])
        if x[1] == '00080000':
            mb_acquisition_conLogic(x,dest_folder,timestr)
##        elif x[1] == '0C004000':  # 
##            mb_acquisition_upper_part_only(x,dest_folder,timestr) # IO data region2 skipped; fetched too slow, and the tag info already in region 1
        else:
            mb_acquisition(x,dest_folder,timestr)


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

    

