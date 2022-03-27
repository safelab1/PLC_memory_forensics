import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)

jlink.connect('LPC2132')

time.sleep(1)

starting = 639*2097152 ################################# PUT the starting address 
for i in range(0,2048):  # 2k files of 2MB
    file_start = starting+ i*2097152
    for j in range (0,256):
    # 256 steps of 8KB each to make a file of 2MB
     
        testfile = open("mem_data_"+str(hex(file_start))+"_end_.txt","a+")

   # if i == 20321:
   #     a = jlink.memory_read(i*10240,99)
   #     b = bytearray(a)
   #     testfile.write(b)
   #     time.sleep(1)
   #     for j in range(100,208):
   #         a = jlink.memory_read(i*10000+j,1)
   #         b = bytearray(a)
   #         testfile.write(b)
   #         time.sleep(0.1)
   #     a = jlink.memory_read(i*10000+208,792)
   #     b = bytearray(a)
   #     testfile.write(b)
   # else:
        a = jlink.memory_read(file_start+j*8192,8192)
        b = bytearray(a)
        testfile.write(b)
  #  type(a)
   # print a
    
        print(file_start+j*8192)
        time.sleep(3)
        testfile.close()
    

