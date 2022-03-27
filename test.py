string = "test test test test"
a =[i for i in range(len(string)) if string.startswith('test', i)]
print a
