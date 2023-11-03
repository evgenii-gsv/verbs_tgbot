import enum


class Emoji(enum.Enum):
    OK = '✅'
    WRONG = '❌'


CORRECT_VERB_ANSWER = Emoji.OK.value + " Correct: {first_form} - {second_form}\n"

INCORRECT_VERB_ANSWER = Emoji.WRONG.value + " Incorrect: the second form of the verb '{first_form}' is not '{wrong_answer}'\n"

HOW_TO = """

Please write only {verbs_quantity} verbs in second form separating them with spaces."""

NEW_VERBS = """\
Here are your {verbs_quantity} irregular verbs for today:

{verbs}""" + HOW_TO

NEW_VERBS_REDEMPTION = """\
A new week of challenge has passed! You've made {error_verbs_quantity} mistakes during this week, and it is time to corret them. Here are your verbs for today:

{verbs}""" + HOW_TO

NEW_VERBS_REDEMPTION_ZERO_MISTAKES = """\
A new week of challenge has passed! You've made no mistakes during this week, congratulations! Here are your {verbs_quantity} verbs for today:

{verbs}""" + HOW_TO

NEW_VERBS_REDEMPTION_LESS_THEN_MIN = """\
A new week of challenge has passed! You've made only {error_verbs_quantity} mistakes during this week, and it is time to correct them. Here are your {verbs_quantity} verbs for today:

{verbs}""" + HOW_TO

INVALID_ANSWER = "Something went wrong... Please try again and make sure you only write {verbs_quantity} words separating them with spaces."

TEACHER_NOTIF_VERBS_SENT = """\
The user @{username} just received these verbs:

{verbs}"""

TEACHER_NOTIF_VERBS_SENT_REDEMPTION = """\
This is the Redemption Arc of the user @{username}. They have made {error_verbs_quantity} mistakes during this week. They just received these verbs:

{verbs}"""

TEACHER_NOTIF_VERBS_ANSWER_RECEIVED = """\
Here are the results of the user @{username}

{result}"""

TRY_AGAIN_VERBS = """
Please try again and write the correct second form of these verbs:

{wrong_verbs}"""

WELCOME_VERBS_CHALLENGE = "Hello, {name}! Welcome to the irregular verbs challange. You will receive {verbs_quantity} verbs once a day at {time}."

SECOND_WELCOME_VERBS_CHALLENGE = "You have already started the challenge! You will receive your verbs at {time}."

PING_RESPONSE = "I'm alive!"