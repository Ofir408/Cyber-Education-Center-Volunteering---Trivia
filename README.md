# Cyber-Education-Center-Volunteering---Trivia
Cyber Education Center (Volunteering) - Trivia Client-Server Project 


# Client - Server Protocol: 

Protocol Documentation
Protocol goes over TCP (choose your port, we use 5678)
Message format:
CCCCCCCCCCCCCCCC|LLLL|MMM...
C = 16 command bytes. The command bytes specify the message TYPE (e.g. LOGIN). The rest is filled with SPACE character (' ').
| - Separator between fields. Mandatory.
L = 4 length bytes. They specify the size of the next field - the message field . A negative value is illegal. Minimal value is 0, Maximal value is 9999.
| - Separator between fields. Mandatory.
M - Message bytes. The message is the data we would like to transfer. Some commands do not require a message field (e.g. LOGOUT). In such a case we would not fill these bytes.
Messages
This section describes the different messages that can be relayed between a client and a server.
Client -> Server
LOGIN
Description: A login request from the user
Command: LOGIN
Message Format: UUU...|PPP...
U - Username
| - Mandatory separator
P - Password
LOGOUT
Description: Log out of the server and terminate the session
Command: LOGOUT
Message Format: Empty
LOGGED
Description: Get a list of currently logged-in users
Command: LOGGED
Message Format: Empty
GET_QUESTION
Description: Get a trivia question from the server
Command: GET_QUESTION
Message Format: Empty
SEND_ANSWER
Description: Send an answer to a question.
Command: SEND_ANSWER
Message Format: id|choice
id - The question index or id. This value is a number.
| - Mandatory Separator.
choice - The answer for the question. This value is a number.
MY_SCORE
Description: Sends the score for the currently logged in user
Command: MY_SCORE
Message Format: Empty
HIGHSCORE
Description: Sends the high score table from the server
Command: HIGHSCORE
Message Format: Empty
Server -> Client
LOGIN_OK
Description: A reply to a LOGIN message, specifying login was successful.
Command: LOGIN_OK
Message Format: Empty
LOGGED_ANSWER
Description: A reply to LOGGED message, sending the list of logged-in users
Command: LOGGED_ANSWER
Message Format: username1, username2, ...
Every logged in user is sent, concatenated by a ', ' separator.
YOUR_QUESTION
Description: A reply to GET_QUESTION message. Sends a trivia question to the user.
Command: YOUR_QUESTION
Message Format: id|question|answer1|answer2|answer3|answer4
id - The question identifier, or number. a numeric value.
question - A string representing the question.
answer1-answer4 - Strings representing the possible answers to the question.
CORRECT_ANSWER
Description: A reply to SEND_ANSWER. Specifies the answer to that question was correct.
Command: CORRECT_ANSWER
Message Format: Empty
WRONG_ANSWER
Description: A reply to SEND_ANSWER. Specifies the answer to that question was incorrect.
Command: WRONG_ANSWER
Message Format: answer
answer - a numeric value, specifying the correct answer.
YOUR_SCORE
Description: A reply to MY_SCORE message. Sends the currently logged-in user score.
Command: YOUR_SCORE
Message Format: score
score - A numeric value representing the current score.
ALL_SCORE
Description: A reply to HIGHSCORE message. Sends the high-score table.
Command: ALL_SCORE
Message Format: user1: score1\nuser2: score2\n...
user1 - The username
score - The user's score
\n - Separator between scores
ERROR
Description: A message specifying an error. When a clients receives this it should drop the connection.
Command: ERROR
Message Format: error_msg
error_msg - A string describing the error. This value can be an empty string.
NO_QUESTIONS
Description: A reply to GET_QUESTION message. Specifies that no more question are available (game is over).
Command: NO_QUESTIONS
Message Format: Empty
Protocol State
The protocol has the following states:
Disconnected
In this state, no communication is taking place between the client and the server.
Connected
In this state, the client's SOCKET is connected to the server, but the client is not logged in yet.
The only message a client can send while in this state is the LOGIN message.
The messages the server can send while in this state are LOGIN_OK to specify a successfull login, and ERROR to specify an error of any kind.
Logged-in
In this state, the client's SOCKET is connected, and the client is LOGGED IN.
The client can send any message while in this state EXCEPT for a LOGIN message.
The server can send any message while in this state EXCEPT for a LOGIN_OK message.

