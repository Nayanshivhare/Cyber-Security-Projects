

# this is the string alphabet it will be used to find char present in msg
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"  # GLOBAL VARIABLE
msg_to_decrypt = input("Enter your msg to encrypt :-")  # GLOBAL VARIABLE

# Looping over ciphershift that is unknown.
# I have taken 25 here because hint is being given in assignment.
x = 0
while x in range(25):
    x += 1

    # for substitution we taking out no. of ciphershft using int.
    ciphershift = int(x)
    msg_aftr_decrypted = ""

    # running loop over all the char in input msg
    for char in msg_to_decrypt:

        # finding position of char in alphabet and then in new position we substitute position of char with ciphershift to get the actual char.
        position = alphabet.find(char)
        newposition = position-ciphershift

        # applied this conditional statement to convert alphabet char and print any other char as it is.
        if char in alphabet:
            msg_aftr_decrypted = msg_aftr_decrypted + alphabet[newposition]
        else:

            msg_aftr_decrypted = msg_aftr_decrypted + char

    print(x, ".", msg_aftr_decrypted)
    print("  ")
