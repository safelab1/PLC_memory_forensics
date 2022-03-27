# Same length files
import time
import os
import struct
import codecs
p = 'C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/one_line_prog/'
entries = os.listdir(p)
print " ---------------------------------------------------------------------------------------------------------------------------------"
print " FILES TO BE SAME IN SIZE: AND TO SHOW CORRECT OFFSET; THE FILE NAMEs SHOULD END AS \".... _startingAddressInHex_to_EndingAddressInHex.bin\""
print " ---------------------------------------------------------------------------------------------------------------------------------"
time.sleep(2)


for entry1 in entries:

    
    fullentry1= os.path.join(p,entry1)
    if os.path.isdir(fullentry1):
        continue
    starting_addr = int(entry1.split("_")[-3],16)
    #print hex(starting_addr)
    f1 = open(fullentry1,'rb')
    f1Arr = f1.read()
    for entry2 in entries:
        fullentry2 = os.path.join(p,entry2)
        if fullentry1 != fullentry2 and not os.path.isdir(fullentry2):
            print (" Checking " +str(entry1) + "  vs  " + entry2)
            f2 = open(fullentry2,'rb')
            f2Arr = f2.read()
            mismatch=0
            i = 0;
            while i < len(f1Arr):
                if(f1Arr[i] != f2Arr[i]):
                    print ("Mismatch no " + str(mismatch) + " at offset " + str(hex(i+starting_addr)) + "  " +  str((f1Arr[i].encode("hex"))) + "  " +  str((f2Arr[i].encode("hex"))) )
            
                    #print(bytearray(f1Arr[i]))
                    mismatch+=1
                i+=1
            f2.close()
    f1.close()

