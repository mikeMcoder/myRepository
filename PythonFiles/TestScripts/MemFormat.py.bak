import sys
print 'Memory Dump Formatter -- Version 2.1 --'
if len(sys.argv) < 2:
    test_name = input('filename("_")')
else:
    test_name = sys.argv[1]
print 'read from file',test_name
test_file = open("%s"%(test_name),"r")
lines = test_file.readlines()
test_file.close()

iter = 16
count = 0
name = test_name.split('.')
test_file = open("%s_mem.txt"%(name[0]),"w")
while count < len(lines):
    
    test_file.write("%0.5X "%(count))
    for i in range(iter):
        try:
            ele = lines[count]
            ele = ele.replace('\r\n','')
            test_file.write(ele+" ")
        except:
            pass
        count += 1
    test_file.write("\n")
test_file.close()
print 'done converting'
    