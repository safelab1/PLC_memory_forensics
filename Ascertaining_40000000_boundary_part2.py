# Value is fast moving at 4000 0054 and 55
# To ascertain if the values are same after every 0x80 bytes (as we observed in 0x4000 0040 th byte
# instead of fetching data every 0x80 bytes, we just check the data at 2 fixed positions repeatedly
# 
import pylink
import time

jlink = pylink.JLink()

jlink.open(-1)
jlink.connect('LPC2132')

addr_1 = 0x40000055
addr_2 = 0x400009d5 # 3 times 80 to observe stable pattern

a_minus_b = []
a_minus_a = []
b_minus_b = []
for i in range(0,30):
    a = jlink.memory_read(addr_1,01)
    b = jlink.memory_read(addr_2,01)
    c = jlink.memory_read(addr_1,01)
    d = jlink.memory_read(addr_2,01)
    e = jlink.memory_read(addr_1,01)
    f = jlink.memory_read(addr_2,01)
    g = jlink.memory_read(addr_1,01)
    h = jlink.memory_read(addr_2,01)
    #time.sleep(0.005)
    #print str(a)+ str(b) + str(c) + str(d)+ str(e) + str(f) +str(g)+ str(h) 
    a_minus_b.append(a[0]-b[0])
    a_minus_b.append(c[0]-d[0])
    a_minus_b.append(e[0]-f[0])
    a_minus_b.append(g[0]-h[0])

    a_minus_a.append(a[0]-c[0])
    a_minus_a.append(c[0]-e[0])
    a_minus_a.append(e[0]-g[0])

    b_minus_b.append(b[0]-d[0])
    b_minus_b.append(d[0]-f[0])
    b_minus_b.append(f[0]-h[0])
j=0
i=0
while i < len(a_minus_b):
    print str(a_minus_b[i]) + " "+ str(a_minus_b[i+1])+" " +str(a_minus_b[i+2])+" " +str(a_minus_b[i+3]) + " a-a " +str(a_minus_a[j]) + " "+ str(a_minus_a[j+1])+" " +str(a_minus_a[j+2])+"  b-b " +str(b_minus_b[j]) + " "+ str(b_minus_b[j+1])+" " +str(b_minus_b[j+2])
    i+=4
    j+=3
