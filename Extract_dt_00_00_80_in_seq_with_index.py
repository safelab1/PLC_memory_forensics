# FIND ADDRESSES AND THE PLACES WHERE THOSE ADDRESSES ARE REFERRED
import time
import os
import struct
import codecs
p = 'C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/code_region/without_program/'
entries = os.listdir(p)
print " ---------------------------------------------------------------------------------------------------------------------------------"
print " FILES TO SHOW CORRECT OFFSET; THE FILE NAMEs SHOULD END AS \".... _startingAddressInHex_to_EndingAddressInHex.bin\""
print " ---------------------------------------------------------------------------------------------------------------------------------"
time.sleep(0.2)

mem_pat_4 = "80"
mem_pat_3 = "00"
mem_pat_2 = "00"
#print mem_pat_3

result_matrix = []
for entry1 in entries:
  
    fullentry1= os.path.join(p,entry1)
    if os.path.isdir(fullentry1):
        continue
    #starting_addr = int(entry1.split("_")[-3],16)
    starting_addr = int(entry1.split("_")[-3],16) #using this line for data extracted after 5000 0000; though it is same as 0x0000 00000
    print "Finding ADDRESSES in file " + entry1
    #print hex(starting_addr)
    f1 = open(fullentry1,'rb')
    f1Arr = f1.read()
    result_matrix.append([])
    i = 1
    j=0
    
    stack_list = []
##    matrix.append([])
##    matrix[0].append([0])
    
    while i < len(f1Arr)-2:

        if(mem_pat_2 == (f1Arr[i].encode("hex"))):
            if(mem_pat_3 == (f1Arr[i+1].encode("hex"))):
                if(mem_pat_4 == (f1Arr[i+2].encode("hex"))):
                    #mem_pat_2 = f1Arr[i-1].encode("hex")
                    mem_pat_1 = f1Arr[i-1].encode("hex")
                    mem_address =  (mem_pat_4 + mem_pat_3 + mem_pat_2 + mem_pat_1)
                    #print (str(hex(i+starting_addr-1))[2:].zfill(8)) +"  "+ str(mem_address )
                    result_matrix[-1].append([])
                    
                    result_matrix[-1][-1].append((str(hex(i+starting_addr-1))[2:].zfill(8)))
                    result_matrix[-1][-1].append(str(mem_address ))
                    
                    j+=1


                    
##                    k=0
##                    if j==0:
##                            matrix.append([])
##                            matrix[j].append([])
##                            matrix[j][0] = mem_address
##                            matrix[j].append(str(hex(i-2+starting_addr)[2:]) )
##                            #print (matrix[j][0]) + " j = " +str(j)
##                            j+=1
##                    else:       
##                        while k < j:
##                            #print " k = " +str(k)
##                            if matrix[k][0] == mem_address:
##                                #print "Match found before j at " +str(k) + " while j was " +str(j)
##                                matrix[k].append(str(hex(i-2+starting_addr)[2:]) )
##                                break
##                            else:
##                                k+=1
##                                continue
##                        if k ==j:
##                            matrix.append([])
##                            matrix[j].append([])
##                            matrix[j][0] = mem_address
##                            matrix[j].append(str(hex(i-2+starting_addr)[2:]) )
##                            #print (matrix[j][0]) + " j = " +str(j)
##                            j+=1
##    
            #print ("Mismatch no " + str(mismatch) + " at offset " + str(hex(i+starting_addr)) + "  " +  str((f1Arr[i].encode("hex"))) + "  " +  str((f2Arr[i].encode("hex"))) )
                
        i+=1
        
    #print len(matrix)
##    print ""
##    print("ADD_IN_DATA REFERRED_FROM_ADDRESSES")
##
##    for x in result_matrix:
##        
##        for y in x:
##            print (y).zfill(8) ,
##        print ""
##    print "Total addresses = " + str(len(matrix))
    print "Total DTs pattern = " +str(j)
    f1.close()
    

p_entry = ""
i=0

#print result_matrix[0]

#print result_matrix
while(i < len(result_matrix[0])):
    for j in result_matrix:
        #print j
        p_entry = p_entry + j[i][0] + " " + j[i][1] +"\t"
    print p_entry
    p_entry =""
    i+=1
    




