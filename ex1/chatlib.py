# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "my_score_msg": "MY_SCORE",
    "get_question": "GET_QUESTION",
    "send_answer": "SEND_ANSWER",
    "get_highscore": "HIGHSCORE",
    "logged_users": "LOGGED"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "score_response_msg": "YOUR_SCORE",
    "question_your_question_msg": "YOUR_QUESTION",
    "question_no_questions_msg": "NO_QUESTIONS",
    "correct_answer": "CORRECT_ANSWER",
    "wrong_answer": "WRONG_ANSWER",
    "all_score": "ALL_SCORE",
    "logged_answer": "LOGGED_ANSWER"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
	Gets command name and data field and creates a valid protocol message
	Returns: str, or None if error occured
	"""

    msg_to_return = ""

    # 16 command bytes.
    # The command bytes specify the message TYPE (e.g. LOGIN). The rest is filled with SPACE character (' ').
    cmd_length = len(cmd)
    if cmd_length > CMD_FIELD_LENGTH:
        return None

    protocol_command_value = cmd
    for _ in range(CMD_FIELD_LENGTH - cmd_length):
        protocol_command_value += " "

    msg_to_return += protocol_command_value + DELIMITER

    # L = 4 length bytes. They specify the size of the next field - the message field.
    # A negative value is illegal. Minimal value is 0, Maximal value is 9999.
    msg_size = len(data)
    if msg_size > 9999:
        return ERROR_RETURN

    msg_size_with_padding = ""
    for _ in range(LENGTH_FIELD_LENGTH - len(str(msg_size))):  # remember : len(str(msg_size))
        msg_size_with_padding += "0"


    msg_to_return += msg_size_with_padding + str(msg_size) + DELIMITER

    # Message bytes. The message is the data we would like to transfer
    msg_to_return += data
    return msg_to_return


def parse_message(data):
    """
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
    parts_of_msg = data.split(DELIMITER, 2)
    if len(parts_of_msg) < 3:
        return None, None

    if len(parts_of_msg) > 3:
        data = DELIMITER.join(parts_of_msg[2:])
    else:
        data = parts_of_msg[-1]
    # validate the size of data
    temp = str(parts_of_msg[-2]).strip().lstrip('0')
    if temp == "":
        temp = "0"

    if str(len(data)) != temp:
        return None, None
    return parts_of_msg[0].strip(), data  # strip


def split_msg(msg, expected_fields):
    """
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's delimiter (|) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
    parts_of_msg = msg.split(DELIMITER)
    if expected_fields != len(parts_of_msg):
        return None
    return [x for x in parts_of_msg]


def join_msg(msg_fields):
    """
	Helper method. Gets a list, joins all of it's fields to one string divided by the delimiter. 
	Returns: string that looks like cell1|cell2|cell3
	"""
    str_to_return = ""
    for current_field in msg_fields:
        str_to_return += str(current_field) + DELIMITER
    return str_to_return[:-1]
