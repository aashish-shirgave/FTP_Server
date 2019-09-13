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

'''
	def get() :
		#get will file to the client
		#TO DO -> 
		#open file 
		#cut file into different parts add header filename and data

	def put() :

'''