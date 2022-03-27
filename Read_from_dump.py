def read_from_dump( list_files, mem_addr , no_of_bytes):
    r_bytes = []

##    print type(no_of_bytes)
##    print "no of bytes = "+ str(no_of_bytes)
    for x in list_files:
        f_st_addr =x[1]
        f_end_addr=x[2]
##        print hex(f_st_addr)
##        print hex(f_end_addr)
##        print type(mem_addr)
        if not isinstance(mem_addr, int):
            req_addr = int(mem_addr,16)
##            print "From Read_from_dump file; mem_addr not integer"
##            print hex(req_addr)
        else:
            req_addr = mem_addr
##            print "From Read_from_dump file; mem_addr is integer; and asg to req_addr"
##            print req_addr
        if req_addr >= f_st_addr and req_addr <= f_end_addr - no_of_bytes:
            st = req_addr - f_st_addr
            end = req_addr - f_st_addr + no_of_bytes
##            print "no of bytes = " + str(no_of_bytes)
##            print "st = " + hex(st)
##            print "end= "+ hex(end)
            r_bytes = x[3][req_addr - f_st_addr : req_addr - f_st_addr + no_of_bytes]
##            print "printing r_bytes"
##            print r_bytes
            return r_bytes
    print "returning FALSE (-1) from 'Read from dump fucntion' for address " + str(hex(mem_addr))
    return (-1)
