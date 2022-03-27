# Finding non-zero bytes in sparsely populated binary files
# if a non-zero byte seen after a chunk of zero bytes, its offset is noted

import string

fname =input("Enter the file name: ")
f = open(fname)
fread = f.read()
fArray = bytearray(fread)
jump_if_non_zero_found = 100

outArray=[]
i=0
while i < len(fArray):
    if fArray[i] != 0:
        outArray.append(i)
        i+=jump_if_non_zero_found
    else:
        i+=1

for i in outArray:
    print hex(i)
    
f.close()
