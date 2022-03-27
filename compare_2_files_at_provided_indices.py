import os
#entries = os.listdir('C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/')
#entries = os.listdir('C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/')

in1 = input("Enter file1 with path: ")
in2 = input("Enter file2 with path: ")
file1 = open(in1,'rb')
file2 = open(in2,'rb')

f1 = file1.read()
f2 = file2.read()

st_1 = input("Enter starting index of file 1 in Hex (eg 0x0A0B) :")
st_2 = input("Enter starting index of file 2 in Hex (eg 0x0A0B) :")

f1_start_index = st_1
f2_start_index = st_2
i=0;
match=0
mismatch=0
print len(f2)
while i<len(f2):
    if f2[i+f2_start_index] == f1[f1_start_index + i]:
       #print ("Mem add " + str (i+f2_start_index) + "MATCHES" + " p5k file offset " + str(i+f1_start_index) + "  MATCH_COUNT= " +str(match+1))
        match+=1
    else:
        print (" File 1 offset " + str(hex(i+f1_start_index)) + " data is " + ((f1[i+f1_start_index]).encode("hex") ) + " NOT_MATCH " + " file 2 offset " + str(hex(i+f2_start_index))  + "  MISMATCH_COUNT= " +str(mismatch+1)) + " data is " + (f2[i+f2_start_index]).encode("hex")
        mismatch+=1
    i+=1
print "Total mismatches = " + str(mismatch)
        
 

