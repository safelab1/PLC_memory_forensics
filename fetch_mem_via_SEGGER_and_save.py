import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)

jlink.connect('LPC2132')

time.sleep(1)

starting = 0000
for i in range(starting,1000000):
     
    testfile = open("mem_data_"+str(starting)+"_end_.txt","a+")

    if i == 20321:
        a = jlink.memory_read(i*10000,99)
        b = bytearray(a)
        testfile.write(b)
        time.sleep(1)
        for j in range(100,208):
            a = jlink.memory_read(i*10000+j,1)
            b = bytearray(a)
            testfile.write(b)
            time.sleep(0.1)
        a = jlink.memory_read(i*10000+208,792)
        b = bytearray(a)
        testfile.write(b)
    else:
        a = jlink.memory_read(i*10000,10000)
        b = bytearray(a)
        testfile.write(b)
  #  type(a)
   # print a
    
    print(i*10000)
    time.sleep(4)
    testfile.close()


