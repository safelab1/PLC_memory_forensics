import os
 
# Finding common sequences from a standard file (eg .p5k and memory dump"

file1='C:\\Users\\SAFE-COMSOL\\Desktop\\jtag\\1756\\viaPython\\SD_CARD\\Logix-Dec11_2020\\CurrentApp\\t1.p5k' # Source file
file2 = 'C:\\Users\\SAFE-COMSOL\\Desktop\\jtag\\1756\\viaPython\\version20_exercise_Dec2020\\mem_sel_range_from_0x50000000_to_0x50ffffff.bin' # Bigger Mem Dump

start_index = 0x0d00000  # starting offset in big file
end_index = 0x0fbffff    # ending offset in big file. 
f1= open(file1, 'rb')
f2= open(file2, 'rb')
f1Array = f1.read()
f2Array = f2.read()

comSeq = [[]]

blocksize = 32
m=0
i=j=0
j_marker = 0

start =0
end = len(f2Array)

while(i < len(f1Array)-blocksize):
    print i
    not_match=False
    for j in range(0,len(f2Array)):
        for k in range(0,blocksize):
            if f1Array[i+k] != f2Array[j+k]:
                not_match=True
                break
        if not_match==False:
            print "Match occured at " + str(i) + " offset in file1 " " and " + str(j) + " offset in dump file (file2)" + " And value is " + str(f1Array[i])
    i+=blocksize
            
        
         
             
         
         

##while i < len(f1Array)-blocksize and j < len(f2Array)-blocksize:
##    not_match = False
##        
##    for k in range(0,blocksize):
##        #print "i= " +str(i) + "  j = "+ str(j) + f1Array[i] + f2Array[j]
##        if f1Array[i+k] != f2Array[j+k]:
##            not_match = True
##            break
##    if not_match == False: # complete window passed, time to try a bigger block
##        print "Match occured at " + str(i) + " offset in file1 " " and " + str(j) + " offset in dump file (file2)" + " And value is " + str(f1Array[i])
##        comSeq.append([i,j])
##        i+=blocksize
##        j+=blocksize
##        j_marker = j
##    else:
##        j+=1
##        if j>=len(f2Array):
##            j=j-marker  # back to the last found out; assuming that match will be in sequence
##            i+=8
##        
##
##f1.close()
##f2.close()
# source is website firmware which is smaller file and is named file1
