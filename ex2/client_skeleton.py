import socket
from ex1 import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


def build_send_recv_parse(conn, cmd, data):
    build_and_send_message(conn, cmd, data)
    return recv_message_and_parse(conn)


def build_and_send_message(conn, code, msg):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    msg_to_send = chatlib.build_message(code, msg)
    print("client send msg to the server:" + msg_to_send)
    print("msg_to_sengd.encode() = " + str(msg_to_send.encode()))
    conn.send(msg_to_send.encode())


def get_score(conn):
    """
    :param conn: socket.
    :return: Nothing. Print the score of this client.
    """

    # Command: YOUR_SCORE, Message Format: score
    # score - A numeric value representing the current score.
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["my_score_msg"], "")
    if cmd != chatlib.PROTOCOL_SERVER["score_response_msg"]:
        print("Failed to get the score from the server")
        return
    print("client score = " + data)


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket.
    Prints debug info, then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    server_response = conn.recv(1024).decode()

    print("server_response= " + server_response)
    cmd, msg = chatlib.parse_message(server_response)
    print("response = " + str(chatlib.parse_message(server_response)))
    return cmd, msg


def connect():
    server_address = (SERVER_IP, SERVER_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    return sock


def error_and_exit(msg):
    print(msg)
    exit(0)


def login(conn):
    was_succeeded = False

    while not was_succeeded:
        username = input("Please enter username:\n")
        password = input("Please enter password:\n")
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],
                               username + chatlib.DELIMITER + password)
        cmd, _ = recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("login successfully")
            was_succeeded = True


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    conn.close()
    exit(0)


def play_question(conn):
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question"], "")
    if cmd == chatlib.PROTOCOL_SERVER["question_no_questions_msg"]:
        print("No more questions")
        return
    # data Message Format: id|question|answer1|answer2|answer3|answer4
    question_id = handle_question(data)
    client_answer = input("Enter your answer\n")
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer"],
                                      str(question_id) + chatlib.DELIMITER + client_answer)
    if cmd == chatlib.PROTOCOL_SERVER["correct_answer"]:
        print("Your answer was correct!\n")
    elif cmd == chatlib.PROTOCOL_SERVER["wrong_answer"]:
        print("Wrong. correct answer is: {0}\n".format(data))


def get_highscore(conn):
    """
    :param conn: socket
    :return: Nothing. prints the highscore table
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_highscore"], "")
    if cmd != chatlib.PROTOCOL_SERVER["all_score"]:
        print("can't print the score table")
        return
    print("Score Table: \n" + data)

def get_logged_users(conn):
    """

    :param conn: socket
    :return: Nothing. Prints the list of the connected users.
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_users"], "")
    if cmd != chatlib.PROTOCOL_SERVER["logged_answer"]:
        print("Failed to load logged users from the server")
        return
    print("Logged Users:\n " + data)

def handle_question(data_msg_format):
    """

    :param data_msg_format: str
    :return: id of the question
    """
    parts = data_msg_format.split(chatlib.DELIMITER)
    if len(parts) != 6:
        print("Invalid question")
        return
    print("Question ID: {0}\n".format(parts[0]))
    print("Question: {0}\n".format(parts[1]))
    for i in range(2, 6):
        print("{0}) {1}\n".format(str(i - 1), parts[i]))
    return parts[0]


def main():
    sock = connect()
    while True:

        user_request_num = int(input("Choose What you want to do:\n1) login \n2) get score\n3) play_question\n"
                                     "4) get highscore table\n5) get logged users\n6) Quit\n"))
        print("user_request_num= " + str(user_request_num))
        if user_request_num == 1:
            login(sock)
        elif user_request_num == 2:
            get_score(sock)
        elif user_request_num == 3:
            play_question(sock)
        elif user_request_num == 4:
            get_highscore(sock)
        elif user_request_num == 5:
            get_logged_users(sock)
        elif user_request_num == 6:
            logout(sock)
        else:
            print("Invalid number.")


if __name__ == '__main__':
    main()


