#Lucas Cunha Peres Rodrigues 83481
#Denis Luciano Lopes 85279
import socket
import threading
import sys

address1='localhost'
class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	id = 0
	
	
	
	def __init__(self,address):
		try:
			
			address1=address
			self.sock.sendto(my_username.encode(),(address, 20000))
		except:
			print("IP inexistente ou indisponível")
			return
			
		cThread = threading.Thread(target=self.sendMsg)
		cThread.daemon = True
		cThread.start()
		print("Conectado com sucesso, envie sua mensagem:\n")
		
		while True:
		
			try:
				data = self.sock.recvfrom(1024)
			except:
				break
			
			#print (data)
			data_string = data[0].decode('utf-8')			
			if not data:
				print('n entrou')
				break
			print(data_string)
		
	def sendMsg(self):
		while True:
			
			msg = input('')
			if msg[:5]=="/file":
				self.sock.sendto(msg.encode(),(address1, 20000))
				sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock2.connect((address1, 20000))
				sock2.send(msg.encode())
				sock2.close()
			elif msg[:4]=="/get":
				self.sock.sendto(msg.encode(),(address1, 20000))
				sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock2.connect((address1, 20000))
				sock2.send(msg.encode())
				sock2.close()
			elif msg[:4]=="/bye":
				self.sock.sendto(msg.encode(),(address1, 20000))
				self.sock.close()
			else:
				self.sock.sendto(msg.encode(),(address1, 20000))

my_username = "Username: "+ input("Username: ")
ip = input('Escreva o endereco IP do servidor no qual voce deseja se conectar (localhost): ')
client = Client(ip)
