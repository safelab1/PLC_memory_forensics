# To extract the two regions of in-use memory bounded by id (markers)
# This is usefull in fetching 'Data and Logic' memory (max 2MB) and IO Data mem max 505,856 max

from Little_endian_conversions import *
import pylink
import time
 



###############################################################
def indexInArray( to_match_this, in_this_array):
    for i in range (len(in_this_array) - len(to_match_this)+1):
        for j in range(len(to_match_this)):
            if to_match_this[j] != in_this_array[i+j]:
                break
        else:
            if(i)%4 == 0:
                return i
    return -1

##############################################333
ii=1
##inList =  [ '00080000', '0027FFFF' , 2048 , 0 , 1 , '80000001' ]
##dest_folder = './'
##timestr='time'
##while ii <2:
##    ii=2
####################################################################
def mb_acquisition(inList , dest_folder, timestr):
    jlink = pylink.JLink()
    jlink.open(-1)
    jlink.connect('LPC2132')

    #jlink.AUTO_JTAG_SPEED=0  # For adapting speed
    #jlink.MAX_TJAG_SPEED = 4000

    #starting_address = 0x50270000  #enter starting hex address
    #ending_address = 0x5027ffff  # enter ending hex address

    p1_start_addr = int(inList[0],16)  
    p1_end_addr = int(inList[0],16)   # will change when mem is fetched from controller
    p2_start_addr = int(inList[1],16)  # will change
    p2_end_addr = int(inList[1],16) # fixed
    chunk_size =inList[2]  # KEEP IN MULTIPLE OF 4
    sleep_duration = inList[4]  # trial
    max_size = 2049000 # as a safety check; not required in program 
##    output =[]
    dt_id=[]
    for i in range(0,len(inList[5])/2):
        dt_id.insert(0,int(inList[5][2*i:2*i+2],16))
    print dt_id
    print (time.strftime("%Y%m%d-%H%M%S"))
    read = (jlink.memory_read(p1_start_addr,len(dt_id)))  
    print read
    if  read != dt_id:
        print "p1_start_addr " + str(hex(p1_start_addr)) + " has data " + str(read) + " which does not match the start sequence " + str(dt_id)
        
    else:
##        print read
        b_read = bytearray(read)
        output = b_read
    ##    for x in b_read:
    ##        output.append(x)
        read = [0]
        i = p1_start_addr  + len(dt_id)
        delta_i=-1
##        print "going for while"
        
        while len(output) < max_size:

            time.sleep(sleep_duration)
            read = jlink.memory_read(i,chunk_size)
##            print read
            delta_i = indexInArray(dt_id,read)
            if delta_i != -1:
                read = read[:delta_i+len(dt_id)]
                b_read = bytearray(read)
##                print "len(read)="+str(len(read))
##                print "i=" +str(hex(i))
##                time.sleep(6)
                i+=len(read)
                for x in b_read:
                    output.append(x)
                
##                print "i=" +str(hex(i))
                break
            else:
                b_read = bytearray(read)
                for x in b_read:
                    output.append(x)
                i+=chunk_size

    ##    if delta_i !=-1:
    ##        read = read[:i+len(dt_id)]
    ##        b_read = bytearray(read) # dt_identifier being added again
    ##        for x in b_read:
    ##            output.append(x)    

    p1_end_addr =  i-1

##    timestr = time.strftime("%Y%m%d-%H%M%S")
    first_block_len = len(output)
    outfile = open(dest_folder+"/"+str(hex(p1_start_addr))[2:].zfill(8)+"_"+str(hex(p1_end_addr))[2:].zfill(8)+"_"+timestr+".bin","ab")
    outfile.write(output)
    outfile.close()



    # NEXT PART FROM BOTTOM TO TOP ##########################################################################################
    #Fetch the data from the end and always append at the last index of the first datastructure

    output2 =[]
    read = jlink.memory_read(p2_end_addr-len(dt_id)+1,len(dt_id))


    if  read != dt_id:
        print "p2_end_addr " + str(hex(p2_end_addr)) + " has data " + str(read) + " which does not match the end sequence " + str(dt_id)
        
    else:
        b_read = bytearray(read)
##        outfile2.seek(0)
##        outfile2.write(b_read)

##        j=0
##        for x in b_read:
##           output2.insert(j,x)
##           j+=1
        output2 = b_read
        
        i= len(dt_id) +chunk_size-1
##        print "i=" +str(hex(i)) + " len of dt_id= "+str(len(dt_id)) + " chunk_size = " +str(chunk_size)
##        time.sleep(5)
        while len(output2) < max_size:

            time.sleep(sleep_duration)
            read = jlink.memory_read(p2_end_addr - i , chunk_size)
##            print read
            delta_i = indexInArray(dt_id,read)
            if delta_i !=-1:
                read = read[delta_i:]
                b_read = bytearray(read)
##                outfile2.seek(0)
##                outfile2.write(b_read)
                j=0
                for x in b_read:
                    output2.insert(j,x)
                    j+=1
                i+=len(read)-chunk_size
                break
            else:
                #print read
                b_read = bytearray(read)
##                outfile2.seek(0)
##                outfile2.write(b_read)
                j=0
                for x in b_read:
                    output2.insert(j,x)
                    j+=1
                i+=chunk_size
    
    p2_start_addr = p2_end_addr - i
##    print str(hex(p2_start_addr)) + "  " + str(hex(p2_end_addr)) + str(hex(i))
##    print(time.strftime("%Y%m%d-%H%M%S"))

    outfile2 = open(dest_folder+"/"+str(hex(p2_start_addr))[2:].zfill(8)+"_"+str(hex(p2_end_addr))[2:].zfill(8)+"_"+timestr+".bin","ab")
    outfile2.write(output2)
    jlink.close()
    outfile2.close()



def mb_acquisition_upper_part_only(inList , dest_folder, timestr):
    jlink = pylink.JLink()
    jlink.open(-1)
    jlink.connect('LPC2132')

    #jlink.AUTO_JTAG_SPEED=0  # For adapting speed
    #jlink.MAX_TJAG_SPEED = 4000

    #starting_address = 0x50270000  #enter starting hex address
    #ending_address = 0x5027ffff  # enter ending hex address

    p1_start_addr = int(inList[0],16)  
    p1_end_addr = int(inList[0],16)   # will change when mem is fetched from controller
    p2_start_addr = int(inList[1],16)  # will change
    p2_end_addr = int(inList[1],16) # fixed
    chunk_size =inList[2]  # KEEP IN MULTIPLE OF 4
    sleep_duration = inList[4]  # trial
    max_size = 2049000 # as a safety check; not required in program 
##    output =[]
    dt_id=[]
    for i in range(0,len(inList[5])/2):
        dt_id.insert(0,int(inList[5][2*i:2*i+2],16))
    print dt_id
    print (time.strftime("%Y%m%d-%H%M%S"))
    read = (jlink.memory_read(p1_start_addr,len(dt_id)))  
    print read
    if  read != dt_id:
        print "p1_start_addr " + str(hex(p1_start_addr)) + " has data " + str(read) + " which does not match the start sequence " + str(dt_id)
        
    else:
##        print read
        b_read = bytearray(read)
        output = b_read
    ##    for x in b_read:
    ##        output.append(x)
        read = [0]
        i = p1_start_addr  + len(dt_id)
        delta_i=-1
##        print "going for while"
        
        while len(output) < max_size:

            time.sleep(sleep_duration)
            read = jlink.memory_read(i,chunk_size)
##            print read
            delta_i = indexInArray(dt_id,read)
            if delta_i != -1:
                read = read[:delta_i+len(dt_id)]
                b_read = bytearray(read)
##                print "len(read)="+str(len(read))
##                print "i=" +str(hex(i))
##                time.sleep(6)
                i+=len(read)
                for x in b_read:
                    output.append(x)
                
##                print "i=" +str(hex(i))
                break
            else:
                b_read = bytearray(read)
                for x in b_read:
                    output.append(x)
                i+=chunk_size

    ##    if delta_i !=-1:
    ##        read = read[:i+len(dt_id)]
    ##        b_read = bytearray(read) # dt_identifier being added again
    ##        for x in b_read:
    ##            output.append(x)    

    p1_end_addr =  i-1

##    timestr = time.strftime("%Y%m%d-%H%M%S")
    first_block_len = len(output)
    outfile = open(dest_folder+"/"+str(hex(p1_start_addr))[2:].zfill(8)+"_"+str(hex(p1_end_addr))[2:].zfill(8)+"_"+timestr+".bin","ab")
    outfile.write(output)
    outfile.close()


#########################################################################################################3
## Specific to control logic
## The marker 80000001 may move up, and PLC does not bother change prev value; therefore it is important to make sure that we fetch the important portions
## a check is added to make sure that logic portion is fetched; and any false marker before the logic is ignored
    
def mb_acquisition_conLogic(inList , dest_folder, timestr):
    jlink = pylink.JLink()
    jlink.open(-1)
    jlink.connect('LPC2132')

    #jlink.AUTO_JTAG_SPEED=0  # For adapting speed
    #jlink.MAX_TJAG_SPEED = 4000

    #starting_address = 0x50270000  #enter starting hex address
    #ending_address = 0x5027ffff  # enter ending hex address

    p1_start_addr = int(inList[0],16)  
    p1_end_addr = int(inList[0],16)   # will change when mem is fetched from controller
    p2_start_addr = int(inList[1],16)  # will change
    p2_end_addr = int(inList[1],16) # fixed
    chunk_size =inList[2]  # KEEP IN MULTIPLE OF 4
    sleep_duration = inList[4]  # trial
    max_size = 2049000 # as a safety check; not required in program 
##    output =[]


   
    dt_id=[]
    for i in range(0,len(inList[5])/2):
        dt_id.insert(0,int(inList[5][2*i:2*i+2],16))
    print dt_id
    print (time.strftime("%Y%m%d-%H%M%S"))
    read = (jlink.memory_read(p1_start_addr,len(dt_id)))  
    print read
    if  read != dt_id:
        print "p1_start_addr " + str(hex(p1_start_addr)) + " has data " + str(read) + " which does not match the start sequence " + str(dt_id)
        
    else:
##        print read
        b_read = bytearray(read)
        output = b_read
    ##    for x in b_read:
    ##        output.append(x)
        read = [0]
        i = p1_start_addr  + len(dt_id)
        delta_i=-1
##        print "going for while"
        
        while len(output) < max_size:

            time.sleep(sleep_duration)
            read = jlink.memory_read(i,chunk_size)
##            print read
            delta_i = indexInArray(dt_id,read)
            if delta_i != -1:
                read = read[:delta_i+len(dt_id)]
                b_read = bytearray(read)
##                print "len(read)="+str(len(read))
##                print "i=" +str(hex(i))
##                time.sleep(6)
                i+=len(read)
                for x in b_read:
                    output.append(x)
                
##                print "i=" +str(hex(i))
                break
            else:
                b_read = bytearray(read)
                for x in b_read:
                    output.append(x)
                i+=chunk_size

    ##    if delta_i !=-1:
    ##        read = read[:i+len(dt_id)]
    ##        b_read = bytearray(read) # dt_identifier being added again
    ##        for x in b_read:
    ##            output.append(x)    

    p1_end_addr =  i-1

##    timestr = time.strftime("%Y%m%d-%H%M%S")
    first_block_len = len(output)
    outfile = open(dest_folder+"/"+str(hex(p1_start_addr))[2:].zfill(8)+"_"+str(hex(p1_end_addr))[2:].zfill(8)+"_"+timestr+".bin","ab")
    outfile.write(output)
    outfile.close()



    # NEXT PART FROM BOTTOM TO TOP ##########################################################################################
    #Fetch the data from the end and always append at the last index of the first datastructure
    temp1 =(jlink.memory_read(0x0027fe5c,4))
    print "printing at 0x27fe5c"
    print temp1
    temp2 =byteArray_to_LE_int(jlink.memory_read(0x0027fe5c,4))
    print hex(temp2)
    minimum_bound = 0x0027FFFF - byteArray_to_LE_int(jlink.memory_read(0x0027fe5c,4))
    print minimum_bound
    output2 =[]
    read = jlink.memory_read(p2_end_addr-len(dt_id)+1,len(dt_id))


    if  read != dt_id:
        print "p2_end_addr " + str(hex(p2_end_addr)) + " has data " + str(read) + " which does not match the end sequence " + str(dt_id)
        
    else:
        b_read = bytearray(read)
##        outfile2.seek(0)
##        outfile2.write(b_read)

##        j=0
##        for x in b_read:
##           output2.insert(j,x)
##           j+=1
        output2 = b_read
        
        i= len(dt_id) +chunk_size-1
##        print "i=" +str(hex(i)) + " len of dt_id= "+str(len(dt_id)) + " chunk_size = " +str(chunk_size)
##        time.sleep(5)
        while len(output2) < max_size:

            time.sleep(sleep_duration)
            read = jlink.memory_read(p2_end_addr - i , chunk_size)
##            print read
            delta_i = indexInArray(dt_id,read)
            if delta_i !=-1 and len(output2) > minimum_bound:
                read = read[delta_i:]
                b_read = bytearray(read)
##                outfile2.seek(0)
##                outfile2.write(b_read)
                j=0
                for x in b_read:
                    output2.insert(j,x)
                    j+=1
                i+=len(read)-chunk_size
                break
            else:
                #print read
                b_read = bytearray(read)
##                outfile2.seek(0)
##                outfile2.write(b_read)
                j=0
                for x in b_read:
                    output2.insert(j,x)
                    j+=1
                i+=chunk_size
    
    p2_start_addr = p2_end_addr - i
##    print str(hex(p2_start_addr)) + "  " + str(hex(p2_end_addr)) + str(hex(i))
##    print(time.strftime("%Y%m%d-%H%M%S"))

    outfile2 = open(dest_folder+"/"+str(hex(p2_start_addr))[2:].zfill(8)+"_"+str(hex(p2_end_addr))[2:].zfill(8)+"_"+timestr+".bin","ab")
    outfile2.write(output2)
    jlink.close()
    outfile2.close()
