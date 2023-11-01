import enum


class Emoji(enum.Enum):
    OK = '✅'
    WRONG = '❌'


CORRECT_VERB_ANSWER = Emoji.OK.value + " Correct: {first_form} - {second_form}\n"

INCORRECT_VERB_ANSWER = Emoji.WRONG.value + " Incorrect: the second form of the verb '{first_form}' is not '{wrong_answer}'\n"

NEW_VERBS = """\
Here is your {verbs_quantity} irregular verbs for today:

{verbs}

Please write only {verbs_quantity} verbs in second form separating them with spaces."""

INVALID_ANSWER = "Something went wrong... Please try again and make sure you only write {verbs_quantity} words separating them with spaces."

TEACHER_NOTIF_VERBS_SENT = """\
The user @{username} just received these verbs:

{verbs}"""

TEACHER_NOTIF_VERBS_ANSWER_RECEIVED = """\
Here are the results of the user @{username}

{result}"""

TRY_AGAIN_VERBS = """
Please try again and write the correct second form of these verbs:

{wrong_verbs}"""

WELCOME_VERBS_CHALLENGE = "Hello, {name}! Welcome to the irregular verbs challange. You will receive {verbs_quantity} verbs once a day at {time}."

SECOND_WELCOME_VERBS_CHALLENGE = "You have already started the challenge! You will receive your verbs at {time}."