from crypt import crypt
import sys


def testPass(cryptPass, dictfile):

    # TODO use the dictionary and crypt to identify possible plaintext passwords that match cryptPass
    salt=cryptPass[:2]
    
    
    #setting u up a dictionary file and reading it.
    dictionary_file=open(dictfile,'r')
    
    #going through all the words in the dictionary 
    for words in dictionary_file.readlines():
    
    #removing space after lines end and getting only word.
        plaintext_password = words.strip('\n')

        #cryptedword can be checked using crypt method.  
        cryptedword= crypt(plaintext_password,salt)


    # If the password is found, use the following:

        #so if crypted word is equal to cryptpass than we can say we found the password.
        if cryptedword==cryptPass:
            print("[+] Found Password: " +plaintext_password+"\n")
            return
    print("[-] Password Not Found.\n")
    return
        


def main(passwdfile,dictfile):
    # TODO take in a password file and a dictionary file and attempt to crack each password in the password file using testPass()

    #reading paswdfile.
    pwd_file=open(passwdfile,'r')

    #reading throughall the line.
    for line in pwd_file.readlines():

        #seprating it after the : so that we can differetiate btwn user and passwrd.
        if ":" in line:

            #spliting victim
            victim=line.split(":")[0]

            #and than spliting the crypted password sotred in the file passwrd with user name.
            cryptPass=line.split(":")[1].strip()
            print("[$$] Cracking passwrd: "+victim)

            #cryptPass="This is a placeholder"

            #giving pass and dictfile in our testpass function.
            testPass(cryptPass, dictfile)

if __name__ == "__main__":
    #command line argument.
    passwdfile=sys.argv[1]
    dictfile=sys.argv[2]
    main(passwdfile,dictfile)
    
    
    
    
