##############################################################################
# server.py
##############################################################################
import random
import socket
from ex1 import chatlib

# GLOBALS
from ex1.chatlib import split_msg, PROTOCOL_SERVER, PROTOCOL_CLIENT, join_msg

users = {}
questions = {}
logged_clients = {}  # a dictionary of client sockets to usernames (logged users) - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    msg_to_send = chatlib.build_message(code, msg)
    print("server send msg to the client:" + msg_to_send)
    conn.send(msg_to_send.encode())


def recv_message_and_parse(conn):
    client_response = conn.recv(1024).decode()
    cmd, msg = chatlib.parse_message(client_response)
    print("client response = " + str(chatlib.parse_message(client_response)))
    return cmd, msg


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file  ## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "How much is 3+3", "answers": ["6", "4", "2", "1"], "correct": 1}
    }

    return questions


def load_user_database():
    """
    Loads users list from file  ## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "abc": {"password": "123", "score": 20, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    # Implement code ...
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', SERVER_PORT))
    sock.listen(1)
    return sock


def send_error(conn, msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], ERROR_MSG + msg)


##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    dict_for_user = users[username]
    score = dict_for_user["score"]
    build_and_send_message(conn, PROTOCOL_SERVER['score_response_msg'], str(score))


# Implement this in later chapters


def handle_logout_message(conn):
    global logged_clients
    host = conn.getpeername()
    if host in logged_clients.keys():
        del logged_clients[host]


# Implement this in later chapters


def handle_login_message(conn, msg):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_clients
    Receives: socket, message code and data
    Returns: None (sends answer to client)
    """
    print("handling login msg..")
    global users  # This is needed to access users dictionary from all functions
    global logged_clients  # To be used later
    client_hostname = conn.getpeername()
    username, password = split_msg(msg, 2)
    if username not in users.keys():
        send_error(conn, 'Username does not exist')
        return
    if users[username]['password'] != password:
        send_error(conn, 'Password is incorrect')
        return
    logged_clients[client_hostname] = username
    build_and_send_message(conn, PROTOCOL_SERVER['login_ok_msg'], '')


def handle_question_message (conn, username):
    random_question = create_random_question(username)
    if random_question is None:
        build_and_send_message(conn, PROTOCOL_SERVER["question_no_questions_msg"], "")
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["question_your_question_msg"], random_question)


def handle_answer_message(conn, username, msg):
    temp = split_msg(msg, 2)
    print("temp = " + str(temp))
    if len(temp) != 2:
        print("Invalid response from the client.")
        return
    question_id = int(temp[0])
    if questions[question_id]['correct'] == int(temp[1]):
        users[username]['score'] += 5
        build_and_send_message(conn, PROTOCOL_SERVER["correct_answer"], '')
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["wrong_answer"],
                               str(questions[question_id]['correct']))


def create_random_question(username):
    # get the questions that this user wasn't be asked yes.
    global users
    global questions
    asked_question_ids = users[username]["questions_asked"]
    all_questions = questions.keys()
    possible_questions = all_questions - asked_question_ids
    if len(possible_questions) == 0:
        print("No question to asked user: ", username)
        return None
    else:
        # get a random question.
        print("possible_questions= " + str(type(possible_questions)))
        random_question_id = random.choice(tuple(possible_questions))
        question = questions[random_question_id]
        question_text, answers = question['question'], question['answers']
        asked_question_ids.append(random_question_id)
        return join_msg([random_question_id, question_text, answers[0], answers[1], answers[2], answers[3]])


def handle_client_message(conn, cmd, msg):
    """
    Gets message code and data and calls the right function to handle command
    Receives: socket, message code and data
    Returns: None
    """
    global logged_clients  # To be used later
    print("cmd = ", cmd)
    if cmd == PROTOCOL_CLIENT['login_msg']:
        handle_login_message(conn, msg)

    add, port = conn.getpeername()
    username = logged_clients[(add, port)]

    if cmd == PROTOCOL_CLIENT['login_msg']:
        return # already handled
    if cmd == PROTOCOL_CLIENT["get_question"]:
        handle_question_message(conn, username)
    elif cmd == PROTOCOL_CLIENT["my_score_msg"]:
        handle_getscore_message(conn, username)
    elif cmd == PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
    elif cmd == PROTOCOL_CLIENT["send_answer"]:
        handle_answer_message(conn, username, msg)
    else:
        send_error(conn, "Invalid Request")


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")
    server_soc = setup_socket()
    client_soc = []
    users = load_user_database()
    questions = load_questions()
    while True:
        print("waiting for a new client to connect...")
        current_client_socket, _ = server_soc.accept()
        client_soc.append(current_client_socket)
        should_continue = True
        while should_continue:
            cmd, msg = recv_message_and_parse(current_client_socket)
            if (cmd == "" or cmd == PROTOCOL_CLIENT["logout_msg"]) and msg == "":
                client_soc.remove(current_client_socket)
                handle_logout_message(current_client_socket)
                current_client_socket.close()
                should_continue = False
            else:
                handle_client_message(current_client_socket, cmd, msg)


if __name__ == '__main__':
    main()
