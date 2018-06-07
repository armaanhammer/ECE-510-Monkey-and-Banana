# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 19:22:06 2018

@author: etcyl
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 18:59:46 2018

@author: etcyl
"""

from prolog import Prolog
import socket
from easy import *

prolog = Prolog()
prolog.consult("final_proj.pl")

host = '192.168.0.104'
port = 5001

mySocket = socket.socket()
mySocket.connect((host,port))

if(bool(list(prolog.query("moveWest(100, 90, 2)")))):
    message = 'right'

mySocket.send(message.encode())
data = mySocket.recv(1024).decode()
print ('Received from server: ' + data)

mySocket.close()
