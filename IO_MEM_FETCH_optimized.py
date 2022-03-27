import pylink
import time

jlink = pylink.JLink()
jlink.MAX_JTAG_SPEED = 4000  ##SLOWED DOWN FOR IO MEM ACCESS
jlink.open(-1)
jlink.connect('LPC2132')
timestr = time.strftime("%Y%m%d-%H%M%S")
dest_folder = './one_line_prog/'

starting_address = 0x0c070000
ending_address = 0x0c07f7ff
chunk_size = 8
sleep_duration =0

output_file = open(dest_folder+"IO_MEM_"+str(timestr) + "_mem_from_"+hex(starting_address)+"_to_"+hex(ending_address)+".bin","ab")

start_decimal = int(starting_address)
end_decimal = int(ending_address)
print (end_decimal - start_decimal )
x= start_decimal
while(x < end_decimal):
    if (end_decimal - x) > chunk_size:
        a = jlink.memory_read(x,chunk_size)
        b = bytearray(a)
       # print b[0],b[1],b[2],b[3]
        output_file.write(b)
        x = x + chunk_size
    else:
        a = jlink.memory_read(x,end_decimal - x+1)
        x = end_decimal
        b = bytearray(a)
        output_file.write(b)
    time.sleep(sleep_duration)
output_file.close()

jlink.close()
