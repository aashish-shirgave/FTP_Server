#title            : client_interface.py
# description     : client side operations of local FTP server
# author          : Aashish Shirgave
# date            : 12/09/2019
# version         : 0.1
# usage           : 
# notes           :
# python_version  : 3.7
##############################
from cmd import Cmd
from sys import exit
from os import system
import constants as const
import socket

class ftp_client(Cmd):
	"""docstring for ftp_client"""
	host_ip = ''
	host_port = 0
	ftp_socket = ''

	prompt = "ftp> "
	download_folder = "./CLIENT_DATA"

	def store_details(self, ftp_soc, ip_address, port = 0) :
		
		self.ftp_socket = ftp_soc
		self.host_ip = ip_address
		self.host_port = port

	def do_ls(self, args) :
		responce = self.run_command(const.LS)
		
		print(responce)

	def do_cd(self, args) :
		print(args)
		print(type(args))
		responce = self.run_command(const.CD + " " + args)
		print(responce)

	def do_mkdir(self, args):
		responce = self.run_command(const.MKDIR + " " + args)
		print(responce)

	def do_cwd(self, args) :
		responce = self.run_command(const.CWD)
		print(responce)

	def do_get(self, args) :
		#send command to server
		command = const.GET + " " + args
		command = command.encode()
		self.ftp_socket.send(command)
		#wait for receiving file
		self.receive_file()
		
	def run_command(self, command) :
		command = command.encode()
		self.ftp_socket.send(command)
		res = self.ftp_socket.recv(const.BUFFER_SIZE)
		res= res.decode()
		return res

	def receive_file(self) :

		transfer_port = ''
		transfer_port = self.ftp_socket.recv(const.BUFFER_SIZE)
		#transfer_port = self.receive_bytes(self.ftp_socket, const.FILEHEADER_SIZE)
		if not transfer_port :
			print("Transfer port not received")
		if transfer_port.decode() == "-1" :
			print("File Not Found : ")
			return
		ack = "YES"
		ack = ack.encode()
		self.ftp_socket.send(ack)
		print(transfer_port)
		

		if transfer_port :
			transfer_port = int(transfer_port)
			#establish a connection between host(server) and client(this) 
			ftp_transfer_socket = self.create_socket(self.host_ip, transfer_port)

			if ftp_transfer_socket :

				filename_header = self.receive_bytes(ftp_transfer_socket, const.FILENAME_SIZE)
				filename = filename_header.decode()
				filename = filename.translate({ord('0') : ''})

				filesize_header = self.receive_bytes(ftp_transfer_socket, const.FILEHEADER_SIZE)
				file_size = int(filesize_header.decode())

				print("Receiving ", file_size, " Bytes of data")

				file_data = self.receive_bytes(ftp_transfer_socket, file_size)
				filepath = self.download_folder + "/" + filename

				transferfile = open(filepath, "wb")
				transferfile.write(file_data)
				transferfile.close()

		else :
			print("no transfer port")


	def receive_bytes(self, ftp_socket, size = None):
		#receives size number of bytes from server

		if ftp_socket and size :
			temp_buffer = ""
			received= b''

			#read input
			while len(temp_buffer) < size :
				temp_buffer = ftp_socket.recv(size)

				if not temp_buffer :
					print("No Bytes Received from server")
				#temp_buffer = temp_buffer.decode()
				print(type(temp_buffer))
				received += temp_buffer[0:]

			return received

		else :
			print("Error : Size or socket not defined")





	def create_socket(self, ip_address, port) :
		try:
			create_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			create_socket.connect((ip_address, port))
			print("Connection to server has been established on port ", port)
		except socket.error as e:
			print("Socket error : ", e )
			return
		return create_socket

