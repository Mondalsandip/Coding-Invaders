filename='/Users/amit.aricent/Documents/Python/test/CollectRequest/amit.txt'

#create and write a file
# with open(filename,'a') as f:
#     f.write('hello')
#
# #read a file
# with open(filename,'r') as f:
#     print(f.read())
#
# #delete a filed
# import os
# os.remove(filename)

import os
with open(filename, "rb") as file:
    try:
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR)
    except OSError:
        file.seek(0)
    last_line = file.readline().decode()

print(last_line)

