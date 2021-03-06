import SocketServer
import json
import time
import re
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
#Hentet fra http://stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters
def illegalSymbolCheck(strg, search=re.compile(r'[^a-z0-9A-Z]').search):
    return bool(search(strg[0]))

users = {}
history = []

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    def sendToSelf(self, timestamp, sender, response, content):
        json_message = json.dumps({'timestamp': timestamp, 'sender': sender, 'response': response, 'content': content})
        self.connection.send(json_message)

    def sendToAll(self, timestamp, sender, response, content):
        killedUsers=[]
        for key in users:
            try:
                users[key].sendToSelf(timestamp, sender, response, content)
            except:
                print "Removed user: " + key
                killedUsers.append(key)
        for user in killedUsers:
            users.pop(user, None)
    
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """

        global users, history

        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ''
        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            try:
                received_json = json.loads(received_string)
                content = str(received_json["content"])
                request = received_json["request"]

                if(self.username!=''):
                    if(request=="msg"):
                        print("Message received")
                        timestamp = time.strftime("%H:%M:%S")
                        self.sendToAll(timestamp, self.username, "message", content)
                        history.append((timestamp, self.username, content))
                    elif(request=="names"):
                        print("Names requested")
                        namesString="Connected users: "
                        for key in users:
                            namesString+=key + " - "
                        self.sendToSelf(time.strftime("%H:%M:%S"), "server", "info", namesString[0:-1])
                    elif(request=="history"):
                        print("History requested")
                        for msg in history:
                            self.sendToSelf(time.strftime("%H:%M:%S"), "server", "history", msg[0] + " : " + msg[1] + " -> " + msg[2])
                    elif(request=="help"):
                        print("Help requested")
                        self.sendToSelf(time.strftime("%H:%M:%S"), "server", "info", "Supported requests: login <username>, logout,msg <message>, names, help, history")
                    elif(request=="login"):
                        print("ERROR: Already logged in")
                        self.sendToSelf(time.strftime("%H:%M:%S"), "server", "error", "Already logged in")
                    elif(request=="logout"):
                        print("User removed:" + self.username)
                        self.sendToSelf(time.strftime("%H:%M:%S"), "server", "info", "Logout sucessfull")
                        users.pop(self.username, None)
                        self.username=''
                    else:
                        print("ERROR: Unknown request")
                        self.sendToSelf(time.strftime("%H:%M:%S"), "server", "error", "Unknown request")
                else:
                    if(request=="login"):
                        if(content in users.values()):
                            print("ERROR: Username taken")
                            self.sendToSelf(time.strftime("%H:%M:%S"), "server", "error", "Username taken")
                        elif(content==''):
                            print("ERROR: No username given")
                            self.sendToSelf(time.strftime("%H:%M:%S"), "server", "error", "No username given")
                        elif(illegalSymbolCheck(content)):
                            print("ERROR: Illegal symbols in username")
                            self.sendToSelf(time.strftime("%H:%M:%S"), "server", "error", "Illegal symbols in username")
                        else:
                            print("User added: " + content)
                            self.sendToSelf(time.strftime("%H:%M:%S"), "server", "info", "Login sucessfull")
                            self.username=content
                            users[content] = self

                            for msg in history:
                                self.sendToSelf(time.strftime("%H:%M:%S"), "server", "history", msg[0] + " : " + msg[1] + " -> " + msg[2])

                    elif(request=="help"):
                        print("Help requested")
                        self.sendToSelf(time.strftime("%H:%M:%S"), "server", "info", "Supported requests: login <username>, logout,msg <message>, names, help, history")
                    else:
                        print("ERROR: Not logged in")
                        self.sendToSelf(time.strftime("%H:%M:%S"), "server", "error", "Not logged in")

                        
            except ValueError:
                print("Not JSON-Object, closing.")
                self.connection.close()


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
