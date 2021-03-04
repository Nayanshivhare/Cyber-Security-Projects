# A python program to illustrate Caesar Cipher Technique


# A python program to illustrate Caesar Cipher Technique


import optparse


# defined encrpyt function
# taking -m as a msg and -k as key from terminal.
def encrypt(msg, key):

    # empty string to store the msg
    encrypted_msg = ""

    # itrating over all char as a in a length of msg.
    for a in range(len(msg)):

        # created a list so that we can apply isalpha() we cn nt use isalpha on boolean
        char = msg[a]
        # applied isalpha to itrate over alphabets only nd handle spaces and other char.
        if char.isalpha():

            # Check if its upper char
            if char.isupper():

                # its formula used to encrypt
                # starting from inside of the bracket (ord of char+key thn - 65) to know char no.
                # dividing it by 26 to know the remainder which we add with 65 to know exact value
                # In lst we taken out chr of value got from (ord(char) + key-65) % 26 + 65) to know exact letter.
                encrypted_msg += chr((ord(char) + key-65) % 26 + 65)

            # check if its lower char.
            else:
                encrypted_msg += chr((ord(char) + key - 97) % 26 + 97)

        # handle other char apart from alphabet.
        else:
            encrypted_msg += char

    print("Encrypted msg:- ", encrypted_msg)


# for decryption we only put substitution "-" with the key.
# rest code for decrypt remains same.
def decrypt(msg, key):
    decrypted_msg = ""

    for b in range(len(msg)):
        char = msg[b]
        if char.isalpha():

            if char.isupper():
                decrypted_msg += chr((ord(char) - key-65) % 26 + 65)

            else:
                decrypted_msg += chr((ord(char) - key - 97) % 26 + 97)

        else:
            decrypted_msg += char

    print("Decrypted msg:- ", decrypted_msg)


def main():
    parser = optparse.OptionParser(
        "usage%prog " + "-f <decrypt | encrypt> -m <message> -k <key>")
    parser.add_option('-f', dest='function', type='string',
                      help='[ decrypt | encrypt ]')
    parser.add_option('-m', dest='msg', type='string',
                      help='message to encrypt (plaintext) or decrypt (encrypted)')
    parser.add_option('-k', dest='key', type='string',
                      help='cipher key as an string')
    (options, args) = parser.parse_args()
    function = options.function
    if ((function != "encrypt" and function != "decrypt") or function == None):
        print('[-] You must specify a valid function: "encrypt" or "decrypt"')
        exit(0)
    msg = str(options.msg)
    key = int(options.key)
    if (msg == None) | (key == None):
        print('[-] You must specify a message and key.')
        exit(0)
    if function == "encrypt":
        encrypt(msg, key)
    elif function == "decrypt":
        decrypt(msg, key)


if __name__ == '__main__':
    main()
