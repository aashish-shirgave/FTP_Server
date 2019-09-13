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

	def run_command(self, command) :
		command = command.encode()
		self.ftp_socket.send(command)
		res = self.ftp_socket.recv(const.BUFFER_SIZE)
		res= res.decode()
		return res

