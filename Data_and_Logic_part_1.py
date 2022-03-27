# To extract the two regions of code memory that are currently in use
# P1 start from 00080000 and end is flexible
# P2 end at 0027 FFFF, while start is flexible
# 2MB max

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

jlink = pylink.JLink()
jlink.open(-1)
jlink.connect('LPC2132')

# DO CHANGES HERE

dest_folder = './code_region/'

#jlink.AUTO_JTAG_SPEED=0  # For adapting speed
#jlink.MAX_TJAG_SPEED = 4000

#starting_address = 0x50270000  #enter starting hex address
#ending_address = 0x5027ffff  # enter ending hex address

p1_start_addr = 0x00080000 # fixed
p1_end_addr = 0x00080008   # will change when mem is fetched from controller
p2_start_addr = 0x0027fff8  # will change
p2_end_addr = 0x0027ffff  # fixed
chunk_size = 400
sleep_duration = 0.5  # trial##################################################################################
dt_id = [1,0,0,0x80]
output =[]

timestr = time.strftime("%Y%m%d-%H%M")

read = jlink.memory_read(p1_start_addr,len(dt_id))
if  read != dt_id:
    print "p1_start_addr " + str(hex(p1_start_addr)) + " has data " + str(read) + " which does not match the start sequence " + str(dt_id)
else:
    print read
    b_read = bytearray(read)
    output = b_read
##    for x in b_read:
##        output.append(x)
    read = [0]
    i = p1_start_addr  + len(dt_id)
    delta_i=-1
    print "going for while"
    
    while len(output) < 0x20000 : # max zone size

        time.sleep(sleep_duration)
        read = jlink.memory_read(i,chunk_size)
        delta_i = indexInArray(dt_id,read)
        if delta_i != -1:
            read = read[:delta_i+len(dt_id)]
            b_read = bytearray(read)
            i+=len(read)
            for x in b_read:
                output.append(x)
            
            print "i=" +str(i)
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

p1_end_addr = p1_start_addr + i


first_block_len = len(output)

outfile = open(dest_folder+"Data_and_Logic_part_1_"+ " _time_"+str(timestr) + "_from_"+hex(p1_start_addr)+"_to_"+hex(p1_end_addr)+".bin","ab")
outfile.write (output)

outfile.close()

# NEXT DATASTRCUTURE FROM BOTTOM TO TOP ##########################################################################################
#Fetch the data from the end and always append at the last index of the first datastructure

read = jlink.memory_read(p2_end_addr-len(dt_id)+1,len(dt_id))

##print "len of output" + str(len(output))
if  read != dt_id:
    print "p2_end_addr " + str(hex(p2_end_addr)) + " has data " + str(read) + " which does not match the end sequence " + str(dt_id)
else:
    b_read = bytearray(read)
    j=0
    for x in b_read:
       output.insert(first_block_len+j,x)
       j+=1
    i= len(dt_id) +chunk_size-1

    while len(output) < 0x20000:

        time.sleep(sleep_duration)
        read = jlink.memory_read(p2_end_addr - i , chunk_size)
        delta_i = indexInArray(dt_id,read)
        if delta_i !=-1:
            read = read[delta_i:]
            b_read = bytearray(read)
            j=0
            print read
            for x in b_read:
                output.insert(first_block_len+j,x)
                j+=1
                i+=len(read)
            break
        else:
            #print read
            b_read = bytearray(read)
            
            j=0
            for x in b_read:
                output.insert(first_block_len+j,x)
                j+=1
            i+=chunk_size

p2_start_addr = p2_end_addr - i
print(time.strftime("%Y%m%d-%H%M%S"))
outfile = open(dest_folder+"Data_and_Logic_part_1_"+ " _time_"+str(timestr) + "_from_"+hex(p1_start_addr)+"_to_"+hex(p1_end_addr)+ "_AND_from_" +hex(p2_start_addr)+"_to_"+hex(p2_end_addr)+".bin","ab")
outfile.write (output)

outfile.close()



