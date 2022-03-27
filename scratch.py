import pylink
import time
dest_folder = "
jlink = pylink.JLink()
jlink.MAX_TJAG_SPEED = 100  ##SLOWED DOWN FOR IO MEM ACCESS
jlink.open(-1)
jlink.connect('LPC2132')
timestr = time.strftime("%Y%m%d-%H%M%S")
dest_folder = './one_line_prog/'
output_file = open(open(dest_folder+" _time_"+str(timestr) + "_mem_from_"+hex(starting_address)+"_to_"+hex(ending_address)+".bin","ab")
for i in range(0x0c07bab0,0x0c07f7ff):
    output_file.write(bytearray(jlink.memory_read(i,64)))

jlink.close()
