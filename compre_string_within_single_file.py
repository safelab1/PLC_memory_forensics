# It takes one string from the same file and find its occurence and indeces where the string occurs
# Give filename , starting index of string , ending index of string

##### INPUT SECTION ################################
file = 'C:\\Users\\SAFE-COMSOL\\Desktop\\jtag\\1756\\viaPython\\version20_exercise_Dec2020\\mem_sel_range_from_0x60000000_to_0x6000ffff.bin'
toComStart = 0x0000
toComEnd = 0x07ff

#########################################################

f = open(file, 'rb')

fArray = f.read()
print len(fArray)

toCompareArray = fArray[toComStart : toComEnd+1]

indices = [hex(i) for i in range(len(fArray)) if fArray.startswith(toCompareArray, i)]

print (indices)

## Finding indices that differ

##destArray = fArray[0x3800 : 0x4000]
##diff_indices = []
##for i in range(len(destArray)):
##    if destArray[i] != toCompareArray[i]:
##        diff_indices.append(i)
##print (diff_indices)


    
##file2 = 'C:\\Users\\SAFE-COMSOL\\Desktop\\jtag\\1756\\viaPython\\version20_exercise_Dec2020\\mem_sel_range_from_0x60a00000_to_0x60a0ffff.bin'
##f2 = open(file2, 'rb')
##f2Array = f2.read()
##
##indices = [hex(i) for i in range(len(f2Array)) if f2Array.startswith(toCompareArray, i)]
##
##print (indices)
