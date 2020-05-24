# -*- coding: utf-8 -*-
import socket
from threading import Thread
import time
import os
import subprocess
#import urllib2
#from irc import MyIrc

class Minibot:

    def __init__(self, server, port, nick, name, email, channel, password):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # cria um socket para conexao
        self.s.connect((server,port)) #conecta no servidor e porta
        time.sleep(0.5) # espera 0.5 segundos
        self.s.recv(4096) # recebe 4kb do servidor 
        self.nick = nick  # atribui apelido
        self.name = name #atribui nome
        self.email = email #atribui email
        self.data = ''  #container dos dados vindo do servidor
        self.channel = channel #atribui canal
        self.command =  None
	self.password = password
        self.close = False #flag de fechamento 


    def getNick(self):
        return self.nick

    def getServer(self):
        return self.server
    
    def getPort(self):
        return self.port

    def decode(self, string):
        string = string.decode("utf-8")
        string = string.strip('\r\n')
        return string

    def encode(self, string):
        string = bytes(string)
        return string

    def ircSend(self, msg):
        msg = "PRIVMSG {0} :{1}\n".format(self.channel, msg)
        msg = self.encode(msg)
        self.SendCommand(msg)
        return

    def ircMessage(self, person, msg):
        msg = "PRIVMSG {0} :{1}\n".format(person, msg)
        msg = self.encode(msg)
        self.SendCommand(msg)
        return
        
    def ping(self):
        self.SendCommand(bytes("PONG :pings\n", "utf-8"))
	return    

    def runCMD(self, channel, command):
	output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	output, err = output.communicate()
	output = output.decode("utf-8")
	output = output.strip("\n")
	self.sendMessage(channel, output)
	return

    def findChannel(self, message):
	channel = self.channelPattern.findall(message)
	channel = channel[0].strip("!")
	return channel

    def hello(self):
        self.ircSend("Hello!")
        return

    def sendMessage(self, channel, ircMessage):
	self.ircMessage(channel, ircMessage)
        return         
         
    def SendCommand(self, cmd):  # funcao de envio de comandos ao servidor
        comm = cmd + '\r\n' #o comando atribui \r\n (obrigatorio para o servidor responder com sucesso)
        self.s.send(comm) #// envia ao servidor
     
         
    def SendPingResponse(self):  #funcao de envio de ping
        if self.data.find('PING') != -1:  #captura mensagem do servidor e verifica se contem PINNG
            self.SendCommand('PONG ' + self.data.split()[1]) # se tiver envia comando PONG + (numero do tempo em ms?)
            time.sleep(15) #espera 15 segundos pra enviar denovo (se tempo menor pode flooda ro server e te kikar) 
             
    def Parse(self, cmd):  #aqui voce adiciona os comandos pro bot
        tp = cmd.split(' ')
        numargs = len(tp)
        fmt = []
        if numargs == 0:
            self.SendCommand(cmd)
        else:
            for i in range(numargs):
                fmt.append(tp[i] + ' ')
            fmt = ' '.join(fmt)
            self.SendCommand(fmt)
     
     
    def run(self):  #loop principal do bot  para manter vivo
         
        self.SendCommand('NICK ' + self.nick)  #envia pedido de nick
        self.SendCommand('USER ' + self.nick + ' ' + self.name + ' ' + self.email + ' :Irc Python') #cria uma credencial de usuario
        self.SendCommand("PRIVMSG NickServ :identify " + self.password + "\n")
	self.SendCommand('JOIN ' + self.channel) #entra no canal
         
        while self.close == False:
            self.data = self.s.recv(4096)  #data fica recebendo todos dados do servidor e guarda em data
            #cmd = self.data.split(' ')[1];
            #if cmd == '477':
            #   print 'here find'
            
            
            self.SendPingResponse()  #envio de ping e resposta d epong do servidor (se nao responder usuario cai)
            time.sleep(0.5) #espera meio segundo pra "respirar"
            if self.data.find ( '.hi' ) != -1:
                self.SendCommand('PRIVMSG #testec3 :I already said hi...\r\n' )
            elif self.data.find('.clear') != -1:
                os.system("clear")
            elif self.data.find('id') != -1:
                self.runCMD(self.channel,'id')
                #process = subprocess.Popen("id",shell=True, stderr=subprocess.PIPE)
		#output = process.stderr.read()
		#for i in output.splitlines():
		#    print i		
                #out = p.read()
                #self.SendCommand('PRIVMSG #testec3' + out + '\r\n' )
                
            print self.data #imprive tudo que vier do servidor
            
            
            #if self.data.find ('Nickserv') != -1:
             #   print self.data + 'here anything'
         
if __name__ == '__main__':
    servidor = 'irc.freenode.net' #aqui digite seu servidor
    porta = 6667 #aqui sua porta (padrão 6667)
    nick = 'CrazyBot31' #mude para seu nick
    name = 'CrazyBot' #digite seu nome
    email =  'Crazy@gmail.com' #digite seu email
    canal = '#testec3' # coloque seu canal
    password='passwordchat'
    bot = Minibot(servidor ,porta,nick ,name , email, canal, password)     #cria um bot
    bot.run() # roda o loop principal do bot
