import asyncio
import websockets
import json
import socket
import threading
import string
import random
import sys
import time 
import math
import psutil
import http
import urllib
import argparse
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

state = {
    "websocket": None
}

console_colors = {
   "green": "\033[32m",
   "yellow": "\033[33m",
   "blue": "\033[34m",
   "magenta": "\033[35m",
   "cyan": "\033[36m",
   "gray": "\033[90m",
   "red": "\033[91m",
   "bg_red": "\033[41m",
   "white": "\033[37m"
}

def log(text, color="magenta"):
   color_code = console_colors[color]
   print("\033[37m[logdemon]: ", f"{color_code}" + str(text))


class HTTPConnectionHandler(http.server.BaseHTTPRequestHandler):
    def do_GET( self ):
        log("[http] recieved message", "yellow")
        try:
            d = json.loads(urllib.parse.unquote(self.path[1:len(self.path)]))
            WS.instance.broadcast( d )
            self.send_response(code=200, message=None)
            self.end_headers()
        except Exception as e:
            print(f"error while parsing http event: {str(e)}")

class ConnectionHandler (WebSocket):
    clients = []

    def __init__(self, server, sock, address):
        super().__init__( server, sock, address )
        state["websocket"] = self

    def broadcast ( self, msg ):
        c = 0
        for client in ConnectionHandler.clients:
            client.sendMessage( msg )
            log(f"[ws] send to {c}", "magenta")
            c += 1
                
    def handleMessage(self ):
        log("[ws] message recieved", "magenta")

    def handleConnected(self):
        log(f"[ws] connected: { self.address}", "green" )
        for client in ConnectionHandler.clients:
            client.sendMessage(self.address[0] + u' - connected')
        ConnectionHandler.clients.append(self)

    def handleClose(self):
        ConnectionHandler.clients.remove(self)
        log(f"[ws] closed: {self.address,}", "red")
        for client in ConnectionHandler.clients:
            client.sendMessage(self.address[0] + u' - disconnected')

class WS:
    server_started = False
    server = None
    session_id = None
    instance = None

    def __init__ (self):
        WS.instance = self

    def randomword(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def start( self, host="localhost", port=9900 ):
        log(f"[ws] starting websockets server at {host}:{port} ...", "green")
        if WS.server_started:
            log("[ws] server already running. Refusing", "yellow")
            return False

        if WS.session_id == None: WS.session_id = self.randomword(32)

        WS.server_started = True
        t1 = threading.Thread(target=self.run_server, args=( host, str(port) ) )
        t1.daemon = True
        t1.start()
        self.emit("started")

    def run_server ( self, host, port ):
        if ( WS.server != None ):
            log("[ws] server already running", "red")
            return

        log(int(port))
        WS.server = SimpleWebSocketServer( host, int(port), ConnectionHandler )
        WS.server.serveforever()

    def ping ( self ):
        self.emit( "ping" )

    def log ( self, text="...", source="logdemon", color="RED" ):
        self.emit( "log", { "source": source, "text": text,  "color": color } )

    def emit ( self, event_name, payload={} ):
        self.broadcast( {
            "session_id": WS.session_id,
            "timestamp": str(math.floor(time.time() * 1000)),
            "event": event_name,
            "data": payload
        } )


    def broadcast_message ( self, data ):
        log("[ws] broadcasting...")
        for ws in ConnectionHandler.clients:
            try: ws.sendMessage( data )
            except Exception as e: log(f"[ws] error while broadcasting message over websockets: {str(e)}")

    def broadcast ( self, data ):
        log("[ws] broadcasting data...")
        try: 
            data["session_id"] = WS.session_id
            data["thread_id"] = WS.session_id
            data["timestamp"] = str(math.floor(time.time() * 1000))
            self.broadcast_message( json.dumps( data ) )
        except Exception as e: log(f"[ws] error while broadcasting data over websockets: {str(e)}")

def parse_args():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--ws')
        parser.add_argument('--http')
        args = parser.parse_args()
        return args
    except Exception as e: log(f"error occured while parsing arguments: { str(e) }")

def run_http_server ( host, port ):
    log(f"[http] running http server at {host}:{port}...", "green")
    server_address = (host, int(port))
    httpd = http.server.HTTPServer(server_address, HTTPConnectionHandler )
    httpd.serve_forever()

if sys.stdin.isatty():
    args = parse_args()

    if ( args.ws != None ):
        log("[ws] running websocket server...", "green")
        ws_host = args.ws.split(":")[0]
        ws_port = args.ws.split(":")[1]
        ws = WS()
        ws.start( host=ws_host, port=ws_port )

        if ( args.http != None ):
            http_host = args.http.split(":")[0]
            http_port = args.http.split(":")[1]
            t2 = threading.Thread( target=run_http_server, args=( http_host, http_port ) )
            t2.daemon = True
            t2.start()
        else:
            log(f"[http] http server is not running", "yellow")
        while True: ""
    else:
        log(f"invalid websocket server settings: {args}", "red" )


    


    