# Extract potential jump tables
# Criteria for a potential jump table is to have consecutive x number of pointers (4 bytes) into firmware [ x is from user input ]
# Need to know the firmware baseaddress in memroy. Default base address is 00D00000
# INPUT: Extracted firmware binary (2) base address (3) no of consecutive pointers to qualify for the base address
#OUTPUT: A csv file with all tables listed one after other; Each entry in a table has 3 fields- [fileoffset+baseAdd],[data(which is a pointer)]>[data at poinited addr]

import time
from Little_endian_conversions import *
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = raw_input(" Enter the filename: Default is 'extracted_firmware.bin'")
if filename == "":
    filename = 'extracted_firmware.bin'
offset=raw_input( "The default offset set is 00D00000. Enter as 0ABC0 in hex")
if offset=="":
    offset = 0x00d00000  # where firmware starts in th memory
else:
    offset = int(offset,16)
##time.sleep(1)

min_length = input("Enter the min length of address pointers to qualify for the table: ")

f = open(filename, 'rb')

f_read = f.read()
f.close()
temp = bytearray(f_read)
f_bytes=[]
for i in temp:
    f_bytes.append(bytes(i))
    f_bytes[-1] = int(f_bytes[-1])
i=0
jump_table=[]
print "length of f_bytes = " +str(len(f_bytes))
while i <len(f_bytes):
    pattern = byteArray_to_LE_string(f_bytes[i:i+4])
    new_jump_table =[]
    while pattern[0:3]=='00d' or pattern[0:3]=='00e' or pattern[0:3]=='00f' and int(pattern[0:4],16) < 0x00fb :
        
        addr_of_jump_table= str(hex(i+offset))[2:].zfill(8)
        new_jump_table.append([addr_of_jump_table])
##        print new_jump_table
        new_jump_table[-1].append(pattern)
        # Fetching the 1st dword at the address pointer
##        print pattern
##        print hex(i)
        pat_int = int(pattern,16) - offset
##        print hex(pat_int)
##        time.sleep(50)
        first_dword = byteArray_to_LE_string(f_bytes[pat_int:pat_int+4])
        new_jump_table[-1].append(">")
        new_jump_table[-1].append(first_dword)
        
        i+=4
        pattern = byteArray_to_LE_string(f_bytes[i:i+4])

        
    i+=4
    if len(new_jump_table) > min_length:
        jump_table.append(new_jump_table)

f1=open('./important_extracted_data/potential_jump_tables/'+'potential_jump_table'+timestr+'_min_len_of_table_'+str(min_length)+'.csv','w')
i=0
for x in jump_table:
    i+=1
    print "Table No: " + str(i)
    for y in x:
        print y
        f1.write(y[0])
        f1.write(" , ")
        f1.write(y[1])
        f1.write(y[2])
        f1.write(y[3])
        f1.write("\n")
    print "\n"
    table_no = "Table No: " + str(i)
    f1.write(table_no)
    
    f1.write("\n")

print "Total no of tables =" + str(i)
##print "total entries printed = " +str(j)
f1.close()
