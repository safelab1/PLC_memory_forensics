import os
import time
entries = os.listdir("C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/important_extracted_data")
#entries = os.listdir('C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython')

##toMatchFile = open("C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/SD_CARD/Logix-Dec9_2020/CurrentApp/AixProcess.p5k",'rb')
##toMatchArray = toMatchFile.read()
for entry in entries:
    #entry ='C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/'+entry
    entry = "C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/important_extracted_data/"+entry

 #entry ="C:/Users/SAFE-COMSOL/Desktop/jtag/1756/viaPython/version20_exercise_Dec2020/"+entry
    if not os.path.isdir(entry):
        if entry[-3:]=='bin':

            file = open(entry, 'rb')
            #  print "staring test" + (entry)
            b = file.read()
         #a =(b.find(b'\x52\x6F\x75\x74\x69\x6E\x65\x3A\x4D\x61\x69\x6E\x4D\x6F\x64\x75\x6C\x65'))
         #a = (b.find('R35805D45'))
            a = (b.find(b'\x02\x01\xa8\xc0')) # ip address in hex 192.168.1.2
            #a = (b.find(b'\x31\x39\x32\x2e\x31\x36\x38\2e'))
       #  a =(b.find(toMatchArray[1762704 : 1762704+450]))
        # print a
            if(a!=-1):
                print hex(a)
                print(entry)

