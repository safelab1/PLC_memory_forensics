import os
 
# Extract a piece from a binary file"
file1='C:\\Users\\SAFE-COMSOL\\Desktop\\jtag\\1756\\viaPython\\version20_exercise_Dec2020\\mem_sel_range_from_0x50000000_to_0x50ffffff.bin' # Source file
file2 = 'C:\\Users\\SAFE-COMSOL\\Desktop\\jtag\\1756\\viaPython\\version20_exercise_Dec2020\\mem_sel_range_from_0x50d00000_to_0x50fbffff.bin' # Destination File

start_index = 0x0d00000  # starting offset in big file
end_index = 0x0fbffff    # ending offset in big file. 
f1= open(file1, 'rb')
f2= open(file2, 'ab')
f1Array = f1.read()
f2Array = f1Array[start_index:(end_index+1)]
f2.write(f2Array)
f1.close()
f2.close()
# source is website firmware which is smaller file and is named file1
