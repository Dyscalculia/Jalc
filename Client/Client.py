# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        self.host = host
        self.server_port = server_port

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.receiver = MessageReceiver(self, self.connection)
        self.receiver.start()
        #self.login("lol")
        #self.send_names_request()
        #self.send_msg("hei")
        #self.send_help_request()

    def login(self, username):
        payload = json.dumps({"request": "login", "content": username})
        self.send_payload(payload)

    def logout(self):
        payload = json.dumps({"request": "logout"})
        self.send_payload(payload)

    def send_msg(self, msg):
        payload = json.dumps({"request": "msg", "content": msg})
        self.send_payload(payload)

    def send_names_request(self):
        payload = json.dumps({"request": "names"})
        self.send_payload(payload)

    def send_help_request(self):
        payload = json.dumps({"request": "help"})
        self.send_payload(payload)

    def disconnect(self):
        self.logout()
        # Close Connection?

    def receive_message(self, message):
        # TODO: Handle incoming message
        print message

    def send_payload(self, data):
        self.connection.send(data)

        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)

    while True:
        command = raw_input("")
        if command.startswith("login"):
            client.login(command.split(" ")[1])
        elif command.startswith("logout"):
            client.logout()
        elif command.startswith("send"):
            client.send_msg(command.split(" ", 1)[1])
        elif command.startswith("names"):
            client.send_names_request()
        elif command.startswith("help"):
            client.send_help_request()