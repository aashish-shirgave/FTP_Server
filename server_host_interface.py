# title           : server_client_interface.py
# description     :Server side operations of local FTP server
# author          : Aashish Shirgave
# date            : 11/09/2019
# version         : 0.1
# usage           : 
# notes           :
# python_version  : 3.7
##############################
'''
functions to create : 
	get 
	put
	ls 
	send_file 
	receive_file
	sucess_message
	error_message
	
'''
import socket
#from commands import getstatusoutput
import subprocess
import os
import sys
import constants as const
#from commands import getstatusoutput


class ClientInterface():
	"""Server side operations of local FTP server"""
	curr_dir = "/SERVER_DATA"


	def __init__(self, ftp_client, ftp_socket):
		
		self.ftp_client = ftp_client
		self.ftp_socket = ftp_socket
		self.main_folder = os.getcwd() 

	def ls(self) :
		#it will show the files from current directory
		#TO DO -> send command to os get responce 
		result = ""
		result = result.encode()
		
		try :
			os.chdir(self.main_folder + self.curr_dir)
			result = subprocess.Popen("ls -l " , shell=True, stdout=subprocess.PIPE).stdout.read()
			#print(result.decode())
			
			print("SUCESS in ls")
		except :
			print("Unable to perform ls")
	
		#result = getstatusoutput('ls - l ./SERVER_DATA')[1]
		#result = result.encode()
		self.ftp_client.send(result)

	def cd(self, client_request) :
		print(client_request)
		p = client_request.split(" ")[1]

		try :
			if self.curr_dir == "/SERVER_DATA" and p == ".." :
				result = "Cannot change Current directory"
			else :				
				os.chdir(self.main_folder + self.curr_dir)
				#print(self.main_folder + self.curr_dir)
				os.chdir(p)
				dir_new = os.getcwd()
				dir_new = dir_new.replace(self.main_folder, '')
				self.curr_dir = dir_new
				#print(self.main_folder)
				#print(dir_new)
				#print(self.curr_dir)
				result = "directory Changed to " + self.curr_dir
		except : 
			print( sys.exc_info()[0])
			result = "Cannot change Current directory"
		#print(p)
		#result = "YES"

		result = result.encode()
		self.ftp_client.send(result)

	
	def mkdir(self, client_request) :
		#print(client_request)
		p = client_request.split(" ")[1]
		directory =self.main_folder + self.curr_dir +"/" + p
		print(directory)
		result = " "
		try :
			if not os.path.exists(directory):
				os.mkdir(directory)
				result = "New directory created : "+ p + " "
		except :
				result = "Failed to create directory"
		#result = "YES"
		result = result.encode()
		self.ftp_client.send(result)

	def cwd(self) :
		responce = self.curr_dir
		responce = responce.encode()
		self.ftp_client.send(responce)


	def get(self, client_request) :
		#get will file to the client
		#TO DO -> 
		#check for file exist
		#open file 
		#cut file into different parts add header filename and data

		filename = client_request.split(" ")[1]
		filepath = self.main_folder + self.curr_dir+"/" + filename

		exists = os.path.isfile(filepath)
		print(filepath)
		if filename and exists :
			print("Preparing to send file")
			self.send_file(filename, filepath)
			print("File Sent Successfully")
		else :
			err = -1
			err = str(err).encode()
			self.ftp_client.send(err)
			print("Failed to send file")


	def send_file (self,filename, filepath) :

		with open(filepath, 'rb') as file_obj :
			transfer_port = ''


			data = file_obj.read()

			#now we need a port for transfer socket
			try :

				transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				transfer_socket.bind(('', 0))
				transfer_socket.listen(1)
				transfer_port = transfer_socket.getsockname()[1]
			except socket.error as e :
				print(e)
				return

			#now we will send the transfer port details to client
			try :
				print("Sending port to client")
				transfer_port = str(transfer_port).encode()
				self.ftp_client.send(transfer_port)				
				ack = self.ftp_client.recv(const.FILEHEADER_SIZE)
				while not ack :
					print("sending port again")
					#transfer_port = str(transfer_port).encode()
					self.ftp_client.send(transfer_port)
					ack = self.ftp_client.recv(const.FILEHEADER_SIZE)
				print("Port address SENT")
				print(ack.decode())

			except socket.error as e :
				print(e)
				return

			while True :
				print("listening on ", transfer_port)
				ftp_transfer_client , address = transfer_socket.accept()
				print("accepted Connection from " , address)

				if ftp_transfer_client :
					byte_sent = 0 #this will count number of bytes sent

					filename_header = self.buffer_header(filename, const.FILENAME_SIZE)

					filesize_header = self.buffer_header(str(len(data)) , const.FILEHEADER_SIZE)

					filetotaldata = filename_header.encode() + filesize_header.encode() + data

					#filetotaldata = filetotaldata.encode()
					while len(filetotaldata) > byte_sent :
						print(byte_sent)
						try :
							byte_sent += ftp_transfer_client.send(filetotaldata[byte_sent :])

						except socket.error as e :
							print(e)
							return
					
					return		 


	def buffer_header(self, header, size = 10) :
		header = str(header)

		while len(header) < size :
			header = "0" + header

		return header
'''
	def put() :

'''