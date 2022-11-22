from email.message import Message
from email.mime import text
import smtplib
from email.mime.text import MIMEText
import optparse


def sendMail(user, pwd, to, subject):
    # created mimetext to send msg
    mime_msg = MIMEText(
        'BELIEVE IN SOMETHING WITH ALL YOUR HEART IT WILL MANIFEST', 'plain')
    mime_msg['From'] = user
    mime_msg['To'] = to
    mime_msg['Subject'] = subject

    # converting msg into string
    msg = mime_msg . as_string()

    try:
        # connecting to mail server on which we wanna send msg using port 587 because TLS ecryption has default port 587
        mail_server = smtplib.SMTP("smtp.gmail.com", port=587)
        print("[+] Connecting To Mail Server.")

        # encrypting SMTP using transport layer security
        mail_server.starttls()
        print("[+] Starting Encrypted Session.")

       # logging to mail server
        mail_server.login(user, pwd)
        print("[+] Logging Into Mail Server.")

        # sending mail to user
        mail_server.sendmail(user, to, msg)
        print("[+] Sending Mail.")
        print("[+] Mail Sent Successfully.")

        # caliing mail_server to quit after it sends msg so that server can be disconnected.
        mail_server.quit()
    except:
        print("[-] Sending Mail Failed.")


def main():
    parser = optparse.OptionParser('usage%prog ' +
                                   '-t <target email> ' +
                                   '-l <gmail login> -p <gmail password>')
    parser.add_option('-t', dest='tgt', type='string',
                      help='specify target email')
    parser.add_option('-l', dest='user', type='string',
                      help='specify gmail login')
    parser.add_option('-p', dest='pwd', type='string',
                      help='specify gmail password')
    (options, args) = parser.parse_args()

    tgt = options.tgt
    user = options.user
    pwd = options.pwd

    sendMail(user, pwd, tgt, subject="Thought of the day")


if __name__ == '__main__':
    main()
