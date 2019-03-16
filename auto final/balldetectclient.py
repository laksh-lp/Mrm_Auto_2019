import socket
import sys
import os
import time
#os.system('./jetson-inference/build/aarch64/bin/./imagenet-camera --prototxt=$mark1/deploy.prototxt --model=$mark1/snapshot_iter_1230.caffemodel --labels=$mark1/labels.txt --input_blob=data --output_blob=softmax')
HOST,PORT="localhost",50007
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
#s1.connect((HOST,5000))
def getball():
        #s.send(b'L')
        data=str(s.recv(40))
        #print(data)
        return data
#while True:
 #       print(getball())
