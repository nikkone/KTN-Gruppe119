# -*- coding: utf-8 -*-
from threading import Thread
import socket
from Client import *

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """
    Client = None
    Connection = None

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        super(MessageReceiver, self).__init__()

        # Flag to run thread as a deamon
        self.daemon = True
        self.Client = client
        self.Connection = connection
        self.start()

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        message = self.Connection.recv(1024)
        self.Client.receive_message(message)
