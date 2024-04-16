from pathlib import Path
from typing import List, Sequence, Tuple
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from verbs_tgbot.services.exceptions import InvalidAnswer, NotSameLength
from verbs_tgbot.services.irregular_verbs import IrregularVerb
from verbs_tgbot.services import messages
from verbs_tgbot.config_reader import config


def check_answers_and_get_response(verbs: Sequence[IrregularVerb], message: Message) -> Tuple[str, Tuple[IrregularVerb, ...]]:
    """The function to check the user's answer to the verbs challenge and to render the respone"""
    
    response = ''
    wrong_verbs = tuple()
    answers = _parse_answers(message)
    _validate_answers_length(verbs, answers)

    for item in zip(verbs, answers):
        second_form_correct, third_form_correct = _check_both_forms(*item)
        if second_form_correct and third_form_correct:
            response += messages.CORRECT_VERB_ANSWER.format(
                first_form=item[0].first_form, 
                second_form=item[0].second_form, 
                third_form=item[0].third_form
                )
        elif second_form_correct:
            response += messages.INCORRECT_THIRD_FORM_ANSWER.format(
                first_form=item[0].first_form,
                wrong_answer=item[1][1]
            )
            wrong_verbs += item[0],
        elif third_form_correct:
            response += messages.INCORRECT_SECOND_FORM_ANSWER.format(
                first_form=item[0].first_form,
                wrong_answer=item[1][0]
            )
            wrong_verbs += item[0],
        else:
            response += messages.INCORRECT_BOTH_FORMS_ANSWER.format(
                first_form=item[0].first_form,
                wrong_answer=' - '.join(item[1])
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


def get_fsmcontext_of_user(user: dict, dp: Dispatcher, bot: Bot) -> FSMContext:
    """The function return the FSM Context of a specified user"""
    state = FSMContext(
                storage=dp.storage,
                key=StorageKey(
                    chat_id=user['id'],
                    user_id=user['id'],
                    bot_id=bot.id
                ))
    return state


def render_verbs(verbs: Sequence[IrregularVerb]) -> str:
    """The function renders the first form of the verbs for the usage in message templates, every verb is rendered on a new line starting with '- to'"""
    return '\n'.join('- to ' + verb.first_form for verb in verbs)


async def notify_teacher(bot: Bot, text: str, teacher_telegram_id: int | None = None):
    """The function sends the teacher a notification"""
    if teacher_telegram_id is None:
        teacher_telegram_id = config.teacher_telegram_id
    await bot.send_message(teacher_telegram_id, text=text)


def get_redemption_template(error_verbs_quantity: int, verbs_quantity: int, verbs_rendered: str,) -> str:
    if error_verbs_quantity == 0:        
        template = messages.NEW_VERBS_REDEMPTION_ZERO_MISTAKES.format(
            verbs_quantity=str(verbs_quantity),
            verbs=verbs_rendered
        )
    elif error_verbs_quantity >= config.verbs_quantity_per_message:
        template = messages.NEW_VERBS_REDEMPTION.format(
            error_verbs_quantity=str(error_verbs_quantity),
            verbs_quantity=str(verbs_quantity),
            verbs=verbs_rendered
        )
    else:
        template = messages.NEW_VERBS_REDEMPTION_LESS_THEN_MIN.format(
            error_verbs_quantity=str(error_verbs_quantity),
            verbs_quantity=str(verbs_quantity),
            verbs=verbs_rendered
        )
    return template
            

def _validate_answers_length(verbs: Sequence[IrregularVerb], answers: Tuple[Tuple[str, ...], ...]) -> None:
    if len(verbs) != len(answers):
        raise NotSameLength


def _check_second_form(verb: IrregularVerb, answer: str) -> bool:
    answer = answer.lower().strip()
    if answer == verb.second_form:
        return True
    elif verb.first_form == 'be' and (answer == 'was' or answer == 'were' or answer == 'was/were'):
        return True
    return False


def _check_both_forms(verb: IrregularVerb, answer: Tuple[str, ...]) -> List[bool]:
    try: 
        second_form_answer, third_form_answer = answer
    except:
        raise InvalidAnswer
    result = [False, False]
    if second_form_answer == verb.second_form or second_form_answer in verb.second_form.split('/'):
        result[0] = True
    if third_form_answer == verb.third_form or third_form_answer in verb.third_form.split('/'):
        result[1] = True
    return result


def _parse_answers(message: Message) -> Tuple[Tuple[str, ...], ...]:
    if not message.text:
        raise InvalidAnswer
    answers = tuple()
    for verb in map(lambda x: x.lower().strip(), message.text.split(',')):
        answers += (tuple(verb.split())),
    return answers
