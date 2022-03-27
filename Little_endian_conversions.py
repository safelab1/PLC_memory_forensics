# convert 4 bytes in array into a little endian dword string
################################################################
import copy

def byteArray_to_LE_string(byte_array):
##    print "Printing from method 'byteArray_to_LE_string': input rx is "
##    print byte_array
    x=copy.copy(byte_array )
    x.reverse()
    b1=""
    for i in x:
        b1=b1+str(hex(i))[2:].zfill(2)
##    print b1
    return (b1)

# convert 4 bytes in array into a little endian dword integer
#########################################################3

def byteArray_to_LE_int(byte_array):
    x=copy.copy(byte_array )
    x.reverse()
    c=""
    for i in x:
        c=c+str(hex(i))[2:].zfill(2)
    c = int(c,16)
    return (c)

# convert 2 bytes in array into a little endian word integer
#########################################################3

def twoBytes_to_LE_int(byte_array):
    x=copy.copy(byte_array )
    x.reverse()
    c=""
    for i in x:
        c=c+str(hex(i))[2:].zfill(2)
    c = int(c,16)
    return (c)

# convert 6 bytes in array into a little endian dword integer
#########################################################3

def sixBytes_to_LE_int(byte_array):
    x=copy.copy(byte_array )
    x.reverse()
    c=""
    for i in x:
        c=c+str(hex(i))[2:].zfill(2)
    c = int(c,16)
    return (c)


# convert 4 bytes in array into a little endian dword string
################################################################
import copy

def fourBytes_to_LE_string(byte_array):
##    print "Printing from method 'byteArray_to_LE_string': input rx is "
##    print byte_array
    x=copy.copy(byte_array )
    x.reverse()
    b1=""
    for i in x:
        b1=b1+str(hex(i))[2:].zfill(2)
##    print b1
    return (b1)

# convert 4 bytes in array into a little endian dword integer
#########################################################3

def fourBytes_to_LE_int(byte_array):
    x=copy.copy(byte_array )
    x.reverse()
    c=""
    for i in x:
        c=c+str(hex(i))[2:].zfill(2)
    c = int(c,16)
    return (c)
