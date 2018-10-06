import grpc
import chat_pb2_grpc
import chat_pb2
import time
import threading
from concurrent import futures
from collections import OrderedDict
import base64
import hashlib
import yaml

from Crypto import Random
from Crypto.Cipher import AES

def yaml_loader(filepath):
    with open(filepath,"r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath, data):
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)

class ChatServer(chat_pb2_grpc.ChatServerServicer):
    
    def __init__(self):
        # List with all the chat history
        self.chats_alice = []
        self.chats_message = []
        self.chats = []
        self.name = []
        self.receiver = []
        self.LruDict= []
        self.max_size = 10
        
    def ChatStream(self, request: chat_pb2.ChatNote, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages
        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n
               

        # For every client a infinite loop starts (in gRPC's own managed thread)
   
    def SendNote(self, request: chat_pb2.ChatNote, context):
        
        self.chats.append(request)  
        print("[{}] {} {}".format(request.name, request.message, request.receiver))
        # Add it to the chat history
        self.chats_message.append(request.message)
        self.receiver.append(request.receiver)
        self.LruDict.append(request.message)
        if len(self.LruDict)>5:
            self.LruDict.pop()
        print(self.LruDict)
        return chat_pb2.Empty()
        



filepath = "config.yaml"
data = yaml_loader(filepath)
port = data.get('port')
address = data.get('address')
#print(port)
#print(address)
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
chat_pb2_grpc.add_ChatServerServicer_to_server(
    ChatServer(), server)
print('Starting server. Listening on port 3000.')
server.add_insecure_port(address + ':' + str(port))
server.start()
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
        server.stop(0)


# if __name__ == '_main_':
#     serve()
