# -*- coding: utf-8 -*-
import SocketServer
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

client_handlers = []
broadcast_msgs = json.dumps({"timestamp": int(time.time()), "sender": "testTest", "response": "message", "content": "test543"})

def register_clientHandler(clienthandler):
    client_handlers.append(clienthandler)

def handle_login(clienthandler, payload):
    clienthandler.username = payload['content']
    clienthandler.is_logged_in = True
    send_info(clienthandler, "Login successful")
    send_history(clienthandler)

def handle_logout(clienthandler, payload):
    clienthandler.username = "not logged in"
    clienthandler.is_logged_in = False
    send_info(clienthandler, "Logout successful")

def handle_msg(clienthandler, payload):
    send_global_msg(clienthandler.username, payload['content'])

def handle_names(clienthandler, payload):
    send_names(clienthandler)

def handle_help(clienthandler, payload):
    send_info(clienthandler, "TODO: skriv hjelp!!")

def send_info(clienthandler, content):
    payload = json.dumps({"timestamp": int(time.time()), "sender": "server", "response": "info", "content": content})
    clienthandler.send_msg(payload)

def send_global_msg(sender, content):
    global broadcast_msgs
    msg = format_msg(sender, content)
    broadcast_msgs += " " + msg
    for clienthandler in client_handlers:
        clienthandler.send_msg(msg)

def format_msg(sender, content):
    return json.dumps({"timestamp": int(time.time()), "sender": sender, "response": "message", "content": content})

def send_history(clienthandler):
    global broadcast_msgs
    broadcast_msgs = broadcast_msgs.replace("{", "[")
    broadcast_msgs = broadcast_msgs.replace("}", "]")
    payload = json.dumps({"timestamp": int(time.time()), "sender": "server", "response": "history", "content": broadcast_msgs})
    clienthandler.send_msg(payload)

def send_names(clienthandler):
    all_usernames = ""
    for clienthandler in client_handlers:
        all_usernames += clienthandler.username + "\n"
    payload = json.dumps({"timestamp": int(time.time()), "sender": "server", "response": "info", "content": all_usernames})
    clienthandler.send_msg(payload)

possible_requests = {
    'login': handle_login,
    'logout': handle_logout,
    'msg': handle_msg,
    'names': handle_names,
    'help': handle_help
}

def handle_message(clienthandler, payload, loggedin):
    if not loggedin:
        send_info(clienthandler, "Not logged in")
        return
    payload = json.loads(payload) # decode the JSON object
    if payload['request'] in possible_requests:
        possible_requests[payload['request']](clienthandler, payload)
    else:
        # Response not valid
        pass

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """

        self.is_logged_in = False
        self.username = "not logged in"
        register_clientHandler(self)

        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        print "new: " + self.ip + " connected"

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            for json_msg in received_string.split("}"):
                if len(json_msg) > 5:
                    handle_message(self, json_msg + "}", self.is_logged_in)

    def send_msg(self, payload):
        #print "Server sender: " + payload
        self.connection.send(payload)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
