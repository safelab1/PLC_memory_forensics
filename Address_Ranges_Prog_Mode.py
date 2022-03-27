# This file presents the active memory address map that covers the 4GB space
# The 'DONT CARE' bits are eliminated to arrive at minimal but complete capturing
# As capturing can be slow, and may hang the PLC, this exercise is important
# Data and io regions are bounded by markers; there is no data outside those markers; 2 zones; 1st zone start with start_addr, 2nd zone ends with end_addr [ 
# If aware, markers added to avoid  unnec capturing of ZEROs or unused data (in LE dword)
# In some circumstances, it may be required to fetch all memory in search of any
# evidence. In such cases, change the marker to 0
# However, 'Dont care' bits optimization is still helpful
# You may add entries for any address range. Addresses should be in hex


# start_addr , end_addr, chunk_size (bytes) , speed , wait , bound_by_marker

addr_ranges = [ [ '00000000', '0007FFFF' , 8192 , 0 , 4 , 0 ] ,   # Part 1 of 16MB repeated  8 times, and covers till 7FFF FFFF #  Split into 3 parts to exclude Data and Logic part (part 2). That part is extrated slow and via markers
               [ '00080000', '0027FFFF' , 8192 , 0 , 4 , 0 ] ,   # Part 2 of 16MB: Data and logic zone : 2MB in total but due to markers, we extract only used mem; This marker may be removed to fetch some old residual data
                [ '00280000', '00FFFFFF' , 8192 , 0 , 4 , 0 ] ,   # Part 3 of 16MB
                [ '08000000', '08000FFF' , 1024 , 0 , 1 , 0 ] ,  # 4KB - 0 [8 or 9] X  x x x 0   X A B C
                [ '08010080', '0801037F' , 1024 , 0 , 1 , 0 ] ,  # 2nd 4KB first piece ; gaps not readable - 0 [8 or 9] X  x x x 1   X D E F
                [ '08010400', '0801047F' , 1024 , 0 , 1 , 0 ] ,  # 4KB in pieces ; gaps not readable - 0 [8 or 9] X  x x x 1   X D E F
                [ '08010580', '080108FF' , 1024 , 0 , 1 , 0 ] ,  # 4KB in pieces ; gaps not readable - 0 [8 or 9] X  x x x 1   X D E F
                [ '08010980', '08010AFF' , 1024 , 0 , 1 , 0 ] ,  # 4KB in pieces ; gaps not readable - 0 [8 or 9] X  x x x 1   X D E F
                [ '08010C80', '08010D7F' , 1024 , 0 , 1 , 0 ] ,  # 4KB in pieces ; gaps not readable - 0 [8 or 9] X  x x x 1   X D E F
                [ '08010E00', '08010EFF' , 1024 , 0 , 1 , 0 ] ,  # 4KB in pieces ; gaps not readable - 0 [8 or 9] X  x x x 1   X D E F
                [ '0A000000', '0A7FFFFF' , 8192 , 0 , 4 , 0 ] ,   # 8MB repeated 4 times; covers till 0BFF FFFF
                [ '0C000000', '0C003FFF' , 1024 , 0 , 4 , 0 ] ,
               [ '0C004000', '0C07F7FF' , 1024 , 0 , 4 , 0 ] ,  # IO DATA; to be fetched really slow; markers 80000001; from start and end
                [ '0C07F800', '0C07FFFF' , 1024 , 0 , 4 , 0 ] ,
                #'!!' 0c0800000 , 0c081f0f immediately halts the processor [0C and 0D has same data
                [ '0C081F10', '0C08283F' , 256 , 0 , 1 , 0 ] ,  #
                [ '0E000000', '0E000FFF' , 256 , 0 , 1 , 0 ],    # Fast counters with dominently zeros; not sure of the boundary (seems few KB)- same pattern till 0FFF FFFF (most likely due to dont care) 
                [ '10000000', '10000FFF' , 256 , 0 , 1 , 0 ],    # Fast changing data packed with FFFFs. Size not sure - repeated till 13FFFFFF
                 #'!!' '14000000', '17FFFFFF' no data - debugger hangs - seems that region is not assigned
                [ '18000000', '18000FFF' , 256 , 0 , 1 , 0 ],    # Same as 10000000 - continues till 1BFFFFFF
                [ '1C000000', '1C000FFF' , 256 , 0 , 1 , 0 ],    # Similar to 0E000000; This pattern contiues till 1FFFFFFF
                [ '20000000', '20000FFF' , 256 , 0 , 1 , 0 ],    # Fast moving data - 10% non-zero but moving - some patterns repeated more frequently; eg 0c07b35c, 010c0db0, 1f000db4
                [ '30000000', '30000FFF' , 256 , 0 , 1 , 0 ],    # Fast moving - same as 20000000 except the default pattern 0000FFFF insted of 0000 - continues till 37FFFFFF
                [ '38000000', '38000FFF' , 256 , 0 , 1 , 0 ],    # Fast moving - but only changes 6 bytes of dword - '6E' remains constant for entire region - continues till 3FFFFFFF
                [ '40000000', '4000007F' , 64 , 0 , 1 , 0 ],     # Only 128 bytes - Top 5 bits '0100 0' middle 20 dont care, last 7 - covers till 47FF FFFF
                [ '48000000', '48000FFF' , 256 , 0 , 1 , 0 ] ,     # Fast moving sparse data - boundary not sure - trend repeated till 4BFFFFFF
                [ '4C000000', '4C000FFF' , 256 , 0 , 1 , 0 ],    # Fast moving data - default pattern 0000FFFF - continues till 4DFFFFFF
                [ '4E000000', '4E000FFF' , 256 , 0 , 1 , 0 ],    # Similar to 48000000 to 4BFFFFFF - covers till 4FFFFFFF
                # !! 50000000 to 57FFFFFF is same as 00000000 to 07FFFFFF
                # Although 08000000 to 0FFFFFFF is different than 00000000 to 07FFFFFF : BUT 50000000 to 57FFFFFF is same as 58000000 to 5FFFFFFF
                # In other words, 50000000 to 50FFFFFF is repeated 16 times (unlike 00000000 to 00FFFFFF that is repeated 8 tmes
                [ '60000000', '60001FFF' , 256 , 0 , 1 , 0],    # 8KB space filled with the own address of each dword (data changeable via debugger)
                [ '60002000', '600027FF' , 256 , 0 , 1 , 0],


                ####...['00880000','0088FFFF',0,0,0,0]
                ]
                  # 2KB data (changeable; 2 bits dont care matching the 8KB above and making a block of 16KB from 60000000 to 60003FFF - this covers till 67FFFFFF
                # 68000000 onwards not readable and/or not configured ; debugger returns Nil data
                
