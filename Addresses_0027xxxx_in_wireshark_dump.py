# FIND ADDRESSES AND THE PLACES WHERE THOSE ADDRESSES ARE REFERRED
import time
import os
import struct
import codecs
p = 'C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/one_line_prog/wireshark/'
entries = os.listdir(p)
print " ---------------------------------------------------------------------------------------------------------------------------------"
print " INPUT IS THE WIRESHARK DUMPS OF CONTROL LOGIC TRANSFER FROM ENGG SW TO PLC"
print " ---------------------------------------------------------------------------------------------------------------------------------"
time.sleep(0.2)

mem_pat_4 = "00"
mem_pat_3 = "27"
#print mem_pat_3


for entry1 in entries:
  
    fullentry1= os.path.join(p,entry1)
    if os.path.isdir(fullentry1):
        continue
    #starting_addr = int(entry1.split("_")[-3],16)
    starting_addr = 0
    print "Finding ADDRESSES in file " + entry1
    #print hex(starting_addr)
    f1 = open(fullentry1,'rb')
    f1Arr = f1.read()
 
    i = 2
    j=0
    matrix = [[]]
##    matrix.append([])
##    matrix[0].append([0])
    
    while i < len(f1Arr)-1:

        if(mem_pat_3 == (f1Arr[i].encode("hex"))):
            if(mem_pat_4 == (f1Arr[i+1].encode("hex"))):

                mem_pat_2 = f1Arr[i-1].encode("hex")
                mem_pat_1 = f1Arr[i-2].encode("hex")
                mem_address =  (mem_pat_4 + mem_pat_3 + mem_pat_2 + mem_pat_1)
                print (mem_address)
                k=0
                if j==0:
                        matrix.append([])
                        matrix[j].append([])
                        matrix[j][0] = mem_address
                        matrix[j].append(str(hex(i-2+starting_addr)[2:]) )
                        #print (matrix[j][0]) + " j = " +str(j)
                        j+=1
                else:       
                    while k < j:
                        #print " k = " +str(k)
                        if matrix[k][0] == mem_address:
                            #print "Match found before j at " +str(k) + " while j was " +str(j)
                            matrix[k].append(str(hex(i-2+starting_addr)[2:]) )
                            break
                        else:
                            k+=1
                            continue
                    if k ==j:
                        matrix.append([])
                        matrix[j].append([])
                        matrix[j][0] = mem_address
                        matrix[j].append(str(hex(i-2+starting_addr)[2:]) )
                        #print (matrix[j][0]) + " j = " +str(j)
                        j+=1
    
            #print ("Mismatch no " + str(mismatch) + " at offset " + str(hex(i+starting_addr)) + "  " +  str((f1Arr[i].encode("hex"))) + "  " +  str((f2Arr[i].encode("hex"))) )
                
        i+=1
    #print len(matrix)
    print ""
    print("OFFSET IN THE RAW DUMP THAT CONTAINS ALL LAYER HEADERS")

    for x in matrix:
        
        for y in x:
            print (y).zfill(8) ,
        print ""
    print "Total addresses = " + str(len(matrix))
    f1.close()

