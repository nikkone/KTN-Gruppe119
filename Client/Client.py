# -*- coding: utf-8 -*-
import socket
import json
import string
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    new_msg = {"request": None, "content": None}
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host,server_port))
        MessageReceiver(self,self.connection)
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        userinput = raw_input()
        self.processClientInput(userinput)
    def disconnect(self):
        self.connection.close()
        print "Disconnected from server"
        exit(0)

    def receive_message(self, message):
        data = json.loads(message)

    def send_payload(self, data):
        msg = json.dumps(data)
        self.connection.send(msg)
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
