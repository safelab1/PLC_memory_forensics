import pylink
import time
import os

default_wait = 1 # second
default_block = 8192

def acquire_specific_range(dest_folder, timestr, start,end, size, speed, wait, marker_based):
    response_time=[]
    
    print "New range being fetched: from " + start + " to " + end + " Time : " +timestr
    
    if wait !=0:
        wait_time = wait
    else:
       wait_time = default_wait
    if size != 0:
        blocksize = size
    else:
        blocksize = default_block

    if marker_based == 0: # non-marker based acquisition

##        wait_time = 1  #############################################################TESTING ONLY
##        blocksize = 8192 ############################################################TESTING ONLY
        
        jlink = pylink.JLink()
        try:
            jlink.open(-1)
        except:
            print "Unable to connect to debugger via USB ..."
            exit()
        jlink.MAX_BUF_SIZE=500000

        try:
            jlink.connect('LPC2880')
        except:
            print "Unable to connect to PLC via debugger..."
            exit()
        start_addr = int(start,16)
        end_addr = int(end,16)
        i= start_addr
        count=0
        no_of_count_before_writing = 10
        while(i < end_addr):
            
            count+=1
            if count % no_of_count_before_writing ==0:
                jlink.close()       ########################### Trial on Jan 20, for handling the problem of plc disconnection from engg
                print hex(i)[2:].zfill(8)
                f1=open(dest_folder+"/"+ start+"_"+ end+"_response_time_list_"+timestr+".csv",'a')
                while len(response_time) > 0:
                    y = response_time.pop()
                    for j in y:
                        f1.write(str(j))
                        f1.write(",")
                    f1.write("\n")
                f1.close()
                time.sleep(3)
                jlink = pylink.JLink()
                try:
                    jlink.open(-1)
                except:
                    print "Unable to connect to debugger via USB ..."
                    exit()
                jlink.MAX_BUF_SIZE=500000

                try:
                    jlink.connect('LPC2880')
                except:
                    print "Unable to connect to PLC via debugger..."
                    exit()
                
                
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
                f= open(dest_folder+"/"+ start+"_"+ end+"_"+timestr+ ".bin",'ab')
                f.write(b)
                f.close()
                i+=blocksize
            else:
                a = jlink.memory_read(i,end_addr -i+1)
                i = end_addr
                b = bytearray(a)
                f= open(dest_folder+"/"+ start+"_"+ end+"_"+timestr+ ".bin",'ab')
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

    return(1)   

def acquire_specific_range_byListEntry(dest_folder, timestr, x):
    response_time=[]

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
        try:
            jlink.open(-1)
        except:
            print "Unable to connect to debugger via USB ..."
            exit()
        jlink.MAX_BUF_SIZE=500000

        try:
            jlink.connect('LPC2880')
        except:
            print "Unable to connect to PLC via debugger..."
            exit()

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
                try:
                    jlink.open(-1)
                except:
                    print "Unable to connect to debugger via USB ..."
                    exit()
                jlink.MAX_BUF_SIZE=500000

                try:
                    jlink.connect('LPC2880')
                except:
                    print "Unable to connect to PLC via debugger..."
                    exit()
                
                
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
    return (1)
