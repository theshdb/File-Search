import os.path
import time

# print("Last modified: "+  time.ctime(os.path.getmtime("D:\\Test\\Hello.txt")))
print("Created:  " , time.ctime(os.path.getctime("D:\\Test\\Hello.txt")))


# results =[]
# results.clear()
# matches = 0
# records = 0

# temp = {}

# file_index = [(root, files) for root, dirs, files in os.walk("D:\\C") if files]

# #perform serach 
# for path, files in file_index:
#     for file in files:
#         records += 1
#         result = path.replace('\\', '/') + '/' + file
#         results.append(result)

# print(results)
# print("********************************************************************")
# results.sort(key=os.path.getmtime)
# print(results)

# print(list(reversed(results)))