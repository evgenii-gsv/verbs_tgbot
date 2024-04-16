import enum


class Emoji(enum.Enum):
    OK = '✅'
    WRONG = '❌'


CORRECT_VERB_ANSWER = Emoji.OK.value + " Correct: {first_form} - {second_form} - {third_form}\n"

INCORRECT_SECOND_FORM_ANSWER = Emoji.WRONG.value + " Incorrect: the 2nd form of the verb '{first_form}' is not '{wrong_answer}'\n"

INCORRECT_THIRD_FORM_ANSWER = Emoji.WRONG.value + " Incorrect: the 3rd form of the verb '{first_form}' is not '{wrong_answer}'\n"

INCORRECT_BOTH_FORMS_ANSWER = Emoji.WRONG.value + " Incorrect: the 2nd and the 3rd forms of the verb '{first_form}' are not '{wrong_answer}'\n"

HOW_TO = """

Please write only the 2nd and the 3rd forms for each verb separating them with a space. Separate the forms of different verbs with a comma (,).
For example, if you are given verbs 'to be' and 'to have', you need to write this: 'was been, had had'"""

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

INVALID_ANSWER = "Something went wrong... Please try again and make sure you only write two forms per verb separating them with a space, separate different verbs forms with a comma."

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
Please try again and write both correct forms of these verbs:

{wrong_verbs}"""

WELCOME_VERBS_CHALLENGE = "Hello, {name}! Welcome to the irregular verbs challange. You will receive {verbs_quantity} verbs once a day at {time}."

SECOND_WELCOME_VERBS_CHALLENGE = "You have already started the challenge! You will receive your verbs at {time}."

PING_RESPONSE = "I'm alive!"
