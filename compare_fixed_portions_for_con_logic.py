import os
#entries = os.listdir('C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/')
#entries = os.listdir('C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/')

file1 = open("C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/Tag_1.1_20201217-134528 mem_from_0x502777e0_to_0x5027d8e2_JUST_NOTHING.bin",'rb')
file2 = open("C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/Tag_1.1_20201217-133603 mem_from_0x502777e0_to_0x5027d8e2_JUST_NOTHING.bin",'rb')


f1 = file1.read()
f2 = file2.read()

file1.close()
file2.close()

f1_start_index = 0x0; 
f2_start_index = 0x0;
i=0;
match=0
mismatch=0
print len(f2)
while i<len(f2):
    if f2[i+f2_start_index] == f1[f1_start_index + i]:
      #  print ("Mem add " + str (i+f2_start_index) + "MATCHES" + " p5k file offset " + str(i+f1_start_index) + "  MATCH_COUNT= " +str(match+1))
        match+=1
    else:
        print ("Mismatch no " + str(mismatch)+ " at offset " + str(hex (i+f2_start_index)) )
        mismatch+=1
    i+=1
        
 

