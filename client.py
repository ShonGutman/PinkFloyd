import socket
import hashlib

SERVER_PORT = 2629
SERVER_IP = '127.0.0.1'
HEADER_SPLITER = '#'
DATA_SPLITER = '&'
PROTOCOL_REQUEST = "REQUEST$%d&%s"
MIN_OPTION = 1
MAX_OPTION = 9
GET_ALL_ALBUMS = 1
STATISTICS = 9
QUIT = 8
GOOD_PASSWORD = 0


def computeMD5hash(my_string):
    """
    function will encrypt user string to MD5
    :param my_string: user's string
    :type my_string: str
    :return: MD5 encrypted message
    """
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def connect_to_server():
    """
    function will create a TCP socket with the server
    #note: socket must be closed outside function
    :return: server_sock
    :rtype: TCP socket
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SERVER_IP, SERVER_PORT)
    server_sock.connect(server_address)
    return server_sock


def get_user_choice():
    """
    function will get the client's request choice. until it is valid
    :return: choice - user's request choice
    :rtype int
    """
    while True:
        print("""
1 Get All Albums
2 Get Album Songs
3 Get Song Length
4 Get Song Lyrics
5 Get Song Album
6 Search Song By Name
7 Search Song by Lyrics
8 Quit
bonus : enter 9 to get statistics - fifty most common words""")

        try:
            choice = int(input("""Enter number: """))
            if choice < MIN_OPTION or choice > MAX_OPTION:
                continue
            break
        except Exception as e:
            print("error occurred", e)
            continue
    return choice


def get_server_data(response):
    """
    function will get the data of the server's answer
    :param response: server's answer
    :type response: str
    :return: the data
    :rtype str
    """
    return response.split("&")[1]


def main():

    server_sock = connect_to_server()
    print("Hello dear user!\n")
    password = input("Enter password: ")
    # current password is : #Magsh1m!m ( for Shira's eyes only )

    password = computeMD5hash(password)  # encrypt the password
    server_sock.sendall((PROTOCOL_REQUEST % (GOOD_PASSWORD, password)).encode())  # send according to protocol

    if get_server_data(server_sock.recv(4096).decode()) == 'Wrong Password':  # user entered wrong password
        print("Access denied")
        server_sock.close()
        return  # close main

    while True:
        try:
            choice = get_user_choice()
            user_data = ''

            if choice == QUIT:
                server_sock.sendall((PROTOCOL_REQUEST % (choice, '')).encode())
                break
            elif choice != GET_ALL_ALBUMS and choice != STATISTICS:
                user_data = input("Please enter data: ")

            server_sock.sendall((PROTOCOL_REQUEST % (choice, user_data)).encode())  # send according to protocol
            answer = server_sock.recv(4096).decode()

            print('\n')
            print(get_server_data(answer))

        except Exception as e:
            print("Server crushed! ", e)
            break

    server_sock.close()
    print("Thank you for using the Pink-Floyd Server! Bye Bye!")


if __name__ == '__main__':
    main()
