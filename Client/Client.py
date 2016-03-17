import socket                                                                                                                                   
import json                                                                                                                                     
from MessageReceiver import MessageReceiver                                                                                                     

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
        self.connection.connect((host, server_port))                                                                                            
        MessageReceiver(self,self.connection)                                                                                                   
        # TODO: Finish init process with necessary code                                                                                         
        self.run()                                                                                                                              
                                                                                                                                                
    def run(self):                                                                                                                              
        # Initiate the connection to the server                                                                                                 
                                                                                                                                                
        print("Connected..")                                                                                                                    
                                                                                                                                                
        while True:                                                                                                                             
            userinput = raw_input()                                                                                                             
            self.processClientInput(userinput)                                                                                                  
                                                                                                                                                
    def disconnect(self):                                                                                                                       
        self.connection.close()                                                                                                                 
        print("Disconnected from server")                                                                                                       
        exit(0)                                                                                                                                 
                                                                                                                                                
    def receive_message(self, message):                                                                                                         
        try:                                                                                                                                    
                                                                                                                                                
            message_array = message.strip().split("}")                                                                                          
                                                                                                                                                
            for message in message_array[0:-1]:                                                                                                 
                data = json.loads(message + "}")                                                                                                
                                                                                                                                                
                if (data['sender'] == 'server'):                                                                                                
                    message = "{} : {} -> {}".format(data['timestamp'],data['response'].upper(), data['content'])                               
                    print(message)                                                                                                              
                else:                                                                                                                           
                    message = "{} : {} -> {}".format(data['timestamp'],data['sender'],data['content'])                                          
                    print(message)                                                                                                              
                                                                                                                                                
        except:                                                                                                                                 
            print("test")                                                                                                                       
            pass                                                                                                                                
                                                                                                                                                
    def send_payload(self, data):                                                                                                               
        msg = json.dumps(data)                                                                                                                  
        self.connection.send(msg)                                                                                                               
                                                                                                                                                
    def processClientInput(self, userinput):                                                                                                    
                                                                                                                                                
        userinput_array = userinput.split(" ")                                                                                                  
                                                                                                                                                
        new_msg = {}                                                                                                                            
                                                                                                                                                
        new_msg['request'] = userinput_array[0]                                                                                                 
                                                                                                                                                
        new_msg['content'] = " ".join(userinput_array[1:])                                                                                      
                                                                                                                                                
        msg = json.dumps(new_msg, sort_keys=True, indent=4, separators=(',', ': '))                                                             
                                                                                                                                                
        self.connection.send(msg)                                                                                                               
                                                                                                                                                
    # More methods may be needed!                                                                                                               
                                                                                                                                                
                                                                                                                                                
if __name__ == '__main__':                                                                                                                      
    """                                                                                                                                         
    This is the main method and is executed when you type "python Client.py"                                                                    
    in your terminal.                                                                                                                           
                                                                                                                                                
    No alterations are necessary                                                                                                                
    """                                                                                                                                         
    client = Client('localhost', 9998)                                                                                                          
                                                                                                                                                