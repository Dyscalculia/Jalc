# -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import MessageParser

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        Thread.__init__(self)

        # Flag to run thread as a deamon
        self.daemon = True

        self.client = client
        self.connection = connection

        self.msgparser = MessageParser()

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            data = self.connection.recv(2048)
            #print "Klient motttok: " + data
            for json_msg in data.split("}"):
                if len(json_msg) > 5:
                    self.client.receive_message(self.msgparser.parse(json_msg + "}", self))

            
