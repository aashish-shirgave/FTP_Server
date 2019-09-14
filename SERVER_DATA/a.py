#import subprocess
#result = ""
#subprocess.call(["ls", "-l"], stdout= result)
#print(result)
#result = subprocess.Popen("ls -l ./SERVER_DATA", shell=True, stdout=subprocess.PIPE).stdout.read()
#print(result.decode())
import os
directory = "./SERVER_DATA/qq"
if not os.path.exists(directory):
	os.mkdir(directory)
	result = "New directory created : "

else :
	print("not created")