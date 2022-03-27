# Input = A bytearray; and min_size of string; output = list of all strings found as per min length

def strings_in_byteArray(b_array, min):
    result = ""
    out_list=[]
    for c in b_array:
        if c >=0x20 and c <=0x7e:
            result += str(unichr(c))
            continue
        if len(result) >= min:
            out_list.append(result)
        result = ""
    if len(result) >= min:  # catch result at EOF
        out_list.append(result)
    return out_list


import pylink
jlink = pylink.JLink()
jlink.open(-1)
jlink.connect('LPC2102')
a=jlink.memory_read(0x241c0,80)
b=bytearray(a)

s = strings_in_byteArray(b,4)
for x in s:
    print x
