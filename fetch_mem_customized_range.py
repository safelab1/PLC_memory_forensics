# To extract samples across space to identify non ZERO areas in the memory region
import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)
jlink.connect('LPC2132')

# DO CHANGES HERE
tag_number = "_"#"1_RUNG_XIO_XIC_1_2_3_"
tag_value = ""
dest_folder = './one_line_prog/'

jlink.AUTO_JTAG_SPEED=0  # For adapting speed
#jlink.MAX_TJAG_SPEED = 4000

#starting_address = 0x50270000  #enter starting hex address
#ending_address = 0x5027ffff  # enter ending hex address

starting_address = 0x027a8e0
ending_address = 0x0027ffff
chunk_size = 8196
sleep_duration = 4
timestr = time.strftime("%Y%m%d-%H%M%S")

start_decimal = int(starting_address)
end_decimal = int(ending_address)
print (end_decimal - start_decimal )
testfile = open(dest_folder+"_"+tag_number+"_v_" +tag_value+" _time_"+str(timestr) + "_mem_from_"+hex(starting_address)+"_to_"+hex(ending_address)+".bin","ab")
x= start_decimal
while(x < end_decimal):
    if (end_decimal - x) > chunk_size:
        a = jlink.memory_read(x,chunk_size)
        b = bytearray(a)
       # print b[0],b[1],b[2],b[3]
        testfile.write(b)
        x = x + chunk_size
    else:
        a = jlink.memory_read(x,end_decimal - x+1)
        x = end_decimal
        b = bytearray(a)
        testfile.write(b)
    time.sleep(sleep_duration)
testfile.close()

    

