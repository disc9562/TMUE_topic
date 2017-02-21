import socket
import struct
import sys
import os
from bower import bower
import json
#import base64
address = ("0.0.0.0", 5000)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except (socket.error, msg):
    print ('Failed to create socket.Error code:' + str(msg[0]) + ', Error message: ' + msg[1] )
    sys.exit()

print ('Socket Created')
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen(5)

while True:
    bbb = bower()
    (client, addr) = s.accept()
    print ('got connected from', addr[0])
    buf = b''
    data_size = 0
    while len(buf)<4:
        buf += client.recv(4-len(buf))
        print (buf)
    size = struct.unpack('!i', buf)
    print ("receiving %s bytes" % size[0])
    """img = open('./public_html/tst.jpg','wb')
    while True:
      data = client.recv(1024)
      if not data:
        print (data)
        #print (1)
        break
      elif data_size == size[0]:
        break
      data_size += len(data)
      img.write(data)
    img.close()"""
    with open('./public_html/tst.jpg', 'wb') as img:
        while True:
            data = client.recv(1024)
            if not data:
                print(1)
                break
           elif data_size == size[0]:
                break
            data_size += len(data)
            img.write(data)
            #img.write(base64.b64decode(data))
    print ('received, yay!')
    bbb.browser()

    """with open('./public_html/a.json','r+') as data_file:
        data = json.dumps(json.load(data_file)).encode('utf-8')
        client.sendall(data)"""
    client.close()
    print('send json, yay!')
