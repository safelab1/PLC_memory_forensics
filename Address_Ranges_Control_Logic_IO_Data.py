# This file presents the selected memory address map that covers control logic and current IO data portion
# The 'DONT CARE' bits are eliminated to arrive at minimal but complete capturing
# As capturing can be slow, and may hang the PLC, this exercise is important
# Data and io regions are bounded by markers; there is no data outside those markers; 2 zones; 1st zone start with start_addr, 2nd zone ends with end_addr [ 
# If aware, markers added to avoid  unnec capturing of ZEROs or unused data (in LE dword)
# In some circumstances, it may be required to fetch all memory in search of any
# evidence. In such cases, change the marker to 0
# However, 'Dont care' bits optimization is still helpful
# You may add entries for any address range. Addresses should be in hex


# start_addr , end_addr, chunk_size (bytes) , speed , wait , bound_by_marker

addr_ranges = [ [ '00080000', '0027FFFF' , 2048 , 0 , 4 , '80000001' ] ,   #  Data and logic zone : 2MB in total but due to markers, we extract only used mem; This marker may be removed to fetch some old residual data
                [ '0C004000', '0C07F7FF' , 16 , 0 , 4 , '80000001' ] ,  # IO DATA; to be fetched really slow; markers 80000001; from start and end
              ]
                  # 2KB data (changeable; 2 bits dont care matching the 8KB above and making a block of 16KB from 60000000 to 60003FFF - this covers till 67FFFFFF
                # 68000000 onwards not readable and/or not configured ; debugger returns Nil data
                
