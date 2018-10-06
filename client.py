from __future__ import print_function

import random
import threading
from threading import Thread

import grpc

import chat_pb2
import chat_pb2_grpc
import time
import subprocess
import sys
import hashlib
import Crypto.Cipher
from base64 import urlsafe_b64encode, urlsafe_b64decode
from Crypto.Cipher import AES
from Crypto import Random
import base64
import yaml
import datetime

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]


key = 'mysecretpassword'

key = hashlib.sha256(key.encode('utf-8')).digest()


def encrypt(raw):
    raw = pad(raw)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return base64.b64encode( iv + cipher.encrypt( raw.encode('utf8') ) )

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))

def yaml_loader(filepath):
    with open(filepath,"r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath, data):
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)

def listen():
    for note in stub.ChatStream(chat_pb2.ChatNote()):
        if note.receiver in user_list1:
            cipher = 'mysecretpassword' 
            note.message = decrypt(note.message)
            note.message = note.message[7:]
            print("[{},{}],{}".format(note.name, note.receiver, note.message))

def listen1():
    for note in stub.ChatStream(chat_pb2.ChatNote()):
        if note.receiver in user_list2:
            cipher = 'mysecretpassword' 
            note.message = decrypt(note.message)
            note.message = note.message[7:]
            print("[{},{}],{}".format(note.name, note.receiver, note.message))

    
def Send_Message():
    message = chat_pb2.ChatNote(message=input(""))
    #print(message)
    #name = chat_pb2.ChatNote(name=input(""))
    if message is not '':
        n = chat_pb2.ChatNote()
        n.message = str(message)
        cipher = 'mysecretpassword'
        n.message = encrypt(n.message) 
        #print(n.message)
        #cipher_text = encryption_suite.encrypt("A really secret message. Not for prying eyes.")
        #print(cipher_text)
        n.name = str(name)
        n.receiver = str(receiver)
            #print("S[{}],{}".format(n.name, n.message))
        stub.SendNote(n)
    if n.name == n.receiver:
        print("cannot communicate")
        sys.exit()
filepath = "config.yaml"
data = yaml_loader(filepath)
port = data.get('port')
address = data.get('address')
#print(port)
#print(address)
#channel = grpc.insecure_channel('localhost:3000')
channel = grpc.insecure_channel(address + ':' + str(port))
stub = chat_pb2_grpc.ChatServerStub(channel)
s = chat_pb2.ChatNote()
user_list1 = data.get('group1')
user_list2 = data.get('group2')
#user_list1 = ['alice','bob','charlie','eve']
#user_list2 = ['foo','bar','baz','qux']
receiver = sys.argv[1]
print(receiver)

if receiver in user_list1:
    name = 'Group1'
elif receiver in user_list2:
    name = 'Group2'
else:
    print("invalid user")
#print(alreadyloggedin)
if name == 'Group1':
    for i in range(len(user_list1)):
        if receiver in user_list1[i]:
            print("user authenticated")
            thread = threading.Thread(target=listen)
            thread.daemon = True
            thread.start()
            i = 1
            while i>0:
                if i==1:
                    Send_Message()
                    currentDT = datetime.datetime.now()
                    #print (str(currentDT))
                    i = i+1
                else:
                    currentDT1 = datetime.datetime.now()
                    diff = (currentDT1 - currentDT).total_seconds()
                    diff = int(round(diff))
                    #print(diff)
                    Send_Message()
                    i = i+1
                    if diff < 10 and i > 3:
                        print("rate limit is 3 messages for 30 seconds please wait sending....")
                        i = 1
                        currentDT = datetime.datetime.now() 
                        time.sleep(10)
                    
                                

if name == 'Group2':
    for i in range(len(user_list2)):
        if receiver in user_list2[i]:
            print("user authenticated")
            thread = threading.Thread(target=listen1)
            thread.daemon = True
            thread.start()
            i = 1
            while i>0:
                if i==1:
                    Send_Message()
                    currentDT = datetime.datetime.now()
                    #print (str(currentDT))
                    i = i+1
                else:
                    currentDT1 = datetime.datetime.now()
                    diff = (currentDT1 - currentDT).total_seconds()
                    diff = int(round(diff))
                    #print(diff)
                    Send_Message()
                    i = i+1
                    if diff < 10 and i > 3:
                        print("rate limit is 3 messages for 30 seconds please wait sending....")
                        i = 1
                        currentDT = datetime.datetime.now() 
                        time.sleep(10)

print("Invalid user name")






   








    







