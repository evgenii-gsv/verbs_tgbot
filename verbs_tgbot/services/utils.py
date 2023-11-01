from pathlib import Path
from typing import Sequence, Tuple
from aiogram.types import Message
import json

from verbs_tgbot.services.exceptions import InvalidAnswer, NotSameLength
from verbs_tgbot.services.irregular_verbs import IrregularVerb
from verbs_tgbot.services import messages
from verbs_tgbot.config_reader import config


def check_answers_and_get_response(verbs: Sequence[IrregularVerb], message: Message) -> Tuple[str, Tuple[IrregularVerb | None, ...]]:
    """The function to check the user's answer to the verbs challenge and to render the respone"""
    
    response = ''
    wrong_verbs = tuple()
    answers = _parse_answers(message)
    _validate_answers_length(verbs, answers)

    for item in zip(verbs, answers):
        if _check_second_form(*item):
            response += messages.CORRECT_VERB_ANSWER.format(
                first_form=item[0].first_form, second_form=item[0].second_form
                )
        else:
            response += messages.INCORRECT_VERB_ANSWER.format(
                first_form=item[0].first_form, wrong_answer=item[1]
            )
            wrong_verbs += item[0], 
    
    if wrong_verbs:
        response += messages.TRY_AGAIN_VERBS.format(
            wrong_verbs=('\n'.join('- ' + verb.first_form for verb in wrong_verbs))
        )
    return response, wrong_verbs

def get_users_from_file(file: Path | None = None) -> list:
    """The function to get user from json file"""

    if file is None:
        file = config.verb_challenge_users_file
    with open(file) as f:
        users = json.load(f)
    return users

def add_user_to_file(user: dict, file: Path | None = None) -> Tuple[dict, bool]:
    """The function to add user to a json file"""
    if file is None:
        file = config.verb_challenge_users_file
    if not file.exists():
        users = []
    else:
        users = get_users_from_file(file)
        if any(existing_user['id'] == user['id'] for existing_user in users):
            return user, False 
    users.append(user)
    with open(config.verb_challenge_users_file, 'w') as f:
        f.write(json.dumps(users, indent=2, ensure_ascii=False))
    return user, True


def _validate_answers_length(verbs: Sequence[IrregularVerb], answers: Sequence[str]) -> None:
    if len(verbs) != len(answers):
        raise NotSameLength

def _check_second_form(verb: IrregularVerb, answer: str) -> bool:
    answer = answer.lower().strip()
    if answer == verb.second_form:
        return True
    elif verb.first_form == 'be' and (answer == 'was' or answer == 'were' or answer == 'was/were'):
        return True
    return False

def _parse_answers(message: Message) -> Tuple[str, ...]:
    if not message.text:
        raise InvalidAnswer
    return tuple(map(str.lower, message.text.split()))