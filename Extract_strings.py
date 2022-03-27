import string

def strings_in_file(filename, min=4):
##    with open(filename) as f:  # Python 3.x
    with open(filename, "rb") as f:           # Python 2.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result

##s = list(strings("extracted_firmware.bin"))
##for x in s:
##    print x


def strings_in_array(bin_array, min=3):
##    with open(filename) as f:  # Python 3.x
          # Python 2.x
    result = ""

    int_printable =[]

    for i in string.printable:
        int_printable.append(ord(i))


    for c in bin_array:
        if c in int_printable:
            result += str(unichr(c))
            continue
        if len(result) >= min:
            yield result
        result = ""
    if len(result) >= min:  # catch result at EOF
        yield result


##
##s = list(strings("extracted_firmware.bin"))
##for x in s:
##    print x



def strings(filename, min=4):
##    with open(filename) as f:  # Python 3.x
    with open(filename, "rb") as f:           # Python 2.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result

##s = list(strings("extracted_firmware.bin"))
##for x in s:
##    print x
