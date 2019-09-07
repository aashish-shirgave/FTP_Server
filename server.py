import socket
import sys

def create_socket() :
	try :
		global host
		global port
		global s
		host = ""
		port = 9999
		s = socket.socket()
		print("socket created")
	except socket.error as msg :
		print("Error While creating socket : " , str(msg))

#create_socket()
def bind_socket() :
	try :
		global host
		global port
		global s
		host = ""
		s.bind((host,port))
		s.listen(5)
		print("socket binded to port : " , port)
	except socket.error as msg :
		print("Error While creating socket : " , str(msg), "retryting ....")
		bind_socket()

def accept_connection() :
	conn, address = s.accept()
	print("Coonection Successful with IP : ", address[0], " and Port : ", address[1])
	send_command(conn)
	conn.close()

def send_command(conn) :
	while True :
		cmd = input()
		if cmd == 'quit' :
			conn.close()
			s.close()
			sys.exit()
		encoded_string = str.encode(cmd)
		if len(encoded_string) > 0 :
			conn.send(encoded_string)
			client_responce = str(conn.recv(1024), "utf-8")
			print(client_responce, end = "")

def main() :
	create_socket()
	bind_socket()
	accept_connection()

main()