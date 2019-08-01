#Lucas Cunha Peres Rodrigues 83481
#Denis Luciano Lopes 85279
import socket
import threading
import sys
import shutil

class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
	connections = {}
	maxID = 1
	
	def __init__(self):
		self.sock.bind(('localhost', 20000))

	
	def recebearq(self,filename,eu):

		ext = filename.split(".")[-1]
		filename2=filename[:-4]
		try:
			with open(filename,'rb+') as rf:
				with open('C:/Users/Lucas/Desktop/downloads/'+filename2+'.'+ext,'wb+') as wf:
					chunk_size = 1024
					rf_chunk = rf.read(chunk_size)
					while len (rf_chunk) > 0:
						wf.write(rf_chunk)
						rf_chunk=rf.read(chunk_size)
			mensagem= "Você recebeu o arquivo, verifique a sua pasta de downloads"
			self.sock.sendto(mensagem.encode(),eu)
		except FileNotFoundError:
			mensagem= "arquivo n existente no servidor"
			self.sock.sendto(mensagem.encode(),eu)

	def enviaarq(self,filename,eu,d):
		print ("entrou")
		ext = filename.split(".")[-1]
		filename2=filename[:-4]
		try:
			with open(filename,'rb+') as rf:
				with open('C:/Users/Lucas/Desktop/uploads/'+filename2+'.'+ext,'wb+') as wf:
					chunk_size = 1024
					rf_chunk = rf.read(chunk_size)
					while len (rf_chunk) > 0:
						wf.write(rf_chunk)
						rf_chunk=rf.read(chunk_size)
			
			for connection in self.connections.keys():
				
						
				mensagem = str(self.connections[eu])[10:]+" enviou o arquivo: " + filename2+'.'+ext
				self.sock.sendto(mensagem.encode(),connection)
		except FileNotFoundError:
			mensagem= "arquivo n existe"
			self.sock.sendto(mensagem.encode(),eu)

		
	
	def handler(self, c, a):
		while True:
			try:
				
				data = c
			except:
				msg = str(self.connections[c]) + " teve sua conexão interrompida"
				print(msg)
				del self.connections[c]
				c.close()
				for connection in self.connections.keys():
					connection.send(msg.encode())
				break
				
			data_string = data.decode('utf-8')
			
			if not data or data_string == "/bye":
				msg = str(self.connections[a]) + " saiu"
				print(msg)
				del self.connections[a]
				
				for connection in self.connections.keys():
					self.sock.sendto(msg.encode(),connection)
				break
				
			elif data_string == "/list":
				msg = "Clientes conectados: " + ",".join(["%s" % v[10:] for v in self.connections.values()])
				
				for connection in self.connections.keys():
					self.sock.sendto(msg.encode(),connection)
				break





			elif data_string[:5]=="/file":
				nada='nada'
			

			elif data_string[:4]=="/get":
				filename=data_string[5:]
				ext = filename.split(".")[-1]
				filename2=filename[:-4]
				with open(filename,'rb+') as rf:
					with open('C:/Users/Lucas/Desktop/downloads/'+filename2+'.'+ext,'wb+') as wf:
						chunk_size = 1024
						rf_chunk = rf.read(chunk_size)
						while len (rf_chunk) > 0:
							wf.write(rf_chunk)
							rf_chunk=rf.read(chunk_size)
				break
				

				print('Recebeu')

			else:
				if(data_string[:9]!="Username:" and data_string !=''):
					
					msg =  data_string
					for connection in self.connections.keys():
						if(connection == a):
							continue
						
						mensagem = str(self.connections[a])[10:]+": " + msg
						self.sock.sendto(mensagem.encode(),connection)
				break
					
					#self.sock.sendto(msg.encode(),('', 20000))
					
	def run(self):
		print("Aguardando conexao")
		while True:
			c, a = self.sock.recvfrom(1024)
			nick = c.decode()
			#print (nick)
			
			if nick[:5]=="/file":
				sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock2.bind(('localhost', 20000))
				sock2.listen(1)
				d, b = sock2.accept()
				print ("CONEXAO TCP")
				filename=nick[6:]
				self.enviaarq(filename,a,d)
				d.close()
				print("ENCERROU CONEXAO TCP")
			elif  nick[:4]=="/get":
				sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock2.bind(('localhost', 20000))
				sock2.listen(1)
				d, b = sock2.accept()
				print ("CONEXAO TCP")
				filename=nick[5:]
				self.recebearq(filename,a)
				d.close()
				print("ENCERROU CONEXAO TCP")

			else:
				sThread = threading.Thread(target = self.handler, args=(c,a))
				sThread.daemon = True
				sThread.start()
				
				if(nick[:9]=="Username:" ):
					
					if(nick not in self.connections):
						self.connections[a] =nick
						
						
				
						self.maxID = self.maxID + 1
						msg =  str(self.connections[a]) + " conectou"
						for connection in self.connections.keys():
							#print (connection)
							if(connection == c):
								continue
							self.sock.sendto(msg.encode(),connection)
						print(msg)
			
server = Server()
server.run()