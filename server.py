import socket
import data

LISTEN_PORT = 2629
HEADER_SPLITER = '#'
DATA_SPLITER = '&'
PROTOCOL_ANSWER = "ANSWER$%d&%s"
QUIT = 8
FILE_PATH = "Pink_Floyd_DB.txt"
GET_ALL_ALBUMS = 1
FIRST_STATISTIC = 9
PASSWORD = 'ec90000dbc2ab781dc773a9ca54a1665'
GOOD_PASSWORD = 0

FUNCTION_DICT = {1: data.get_all_albums, 2: data.get_all_songs_in_album, 3: data.get_song_length,
                 4: data.get_song_lyrics, 5: data.get_song_album, 6: data.search_song_by_name,
                 7: data.search_song_by_lyrics, 9: data.fifty_most_common}


def get_request_type(message):
    """
    function will find the request code from the client's request
    :param message: the client request
    :type message: str
    :return: int - request code
    """
    return int(''.join(filter(lambda x: '1' <= x <= '9', message)))


def get_user_data(message):
    """
    function will get the data of the client's request
    :param message: client's request
    :type message: str
    :return: the data
    :rtype str
    """
    return message.split("&")[1]


def connect_to_client():
    """
    function will create a TCP socket with the client
    #note: socket must be closed outside function
    :return: server_sock
    :rtype: TCP socket
    """
    print("Waiting for connection . . .")
    server_address = ('', LISTEN_PORT)
    with socket.socket() as listen_sock:
        try:
            listen_sock.bind(server_address)  # try to bind socket to port
        except Exception as e:
            print("error occurred", e)
        listen_sock.listen(1)
        return listen_sock.accept()


def main():

    data_dict = data.create_band_data_structure(FILE_PATH)
    while True:
        try:
            client_sock, client_address = connect_to_client()
            print("Connected to client !\n")
            msg = client_sock.recv(4096).decode()

            if PASSWORD != get_user_data(msg):
                client_sock.sendall((PROTOCOL_ANSWER % (QUIT, "Wrong Password")).encode())  # send according to protocol
                client_sock.close()  # user has no permission to use the server
                break
            else:
                client_sock.sendall((PROTOCOL_ANSWER % (GOOD_PASSWORD, "All Good!")).encode())  # send according to protocol

            while True:
                msg = client_sock.recv(4096).decode()
                choice = get_request_type(msg)
                user_data = get_user_data(msg)

                if choice == QUIT:
                    break
                elif choice == GET_ALL_ALBUMS or choice == FIRST_STATISTIC:
                    answer = FUNCTION_DICT[choice](data_dict)  # use functions in data.py
                else:
                    answer = FUNCTION_DICT[choice](data_dict, user_data)

                client_sock.sendall((PROTOCOL_ANSWER % (choice, answer)).encode())  # send according to protocol

            client_sock.close()
            print("""client %s has disconnected.
connection in port %s has been closed.""" % client_address)

            break
        except Exception as e:
            print("Exception occurred :", e)
            print('\n')


if __name__ == '__main__':
    main()


