from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
from random import sample

from verbs_tgbot.config_reader import config
from verbs_tgbot.services.exceptions import FileWithVerbsNotFound


@dataclass(frozen=True, slots=True)
class IrregularVerb:
    """A dataclass to store information about an irregular verb."""
    
    first_form: str
    second_form: str
    third_form: str

    def __str__(self) -> str:
        return 'to ' + self.first_form

 
def get_all_verbs_from_file(file: Path | None = None) -> Tuple[IrregularVerb, ...]:
    """A function to get all the verbs from the verbs file"""
    if file is None:
        file = config.irregular_verbs_file_path
    try:
        with open(file, 'r') as f:
            tuple_of_verbs = tuple(
                IrregularVerb(*line.split()) for line in f.readlines()
            )
    except FileNotFoundError:
        raise FileWithVerbsNotFound(f'No file containing irregular verbs was found. Make sure {file} exists.')
    return tuple_of_verbs

def get_random_verbs_from_file(verbs_quantity: int | None = None, file: Path | None = None) -> Tuple[IrregularVerb, ...]:
    """A function to get random verbs from the verbs file"""
    if verbs_quantity is None:
        verbs_quantity = config.verbs_quantity_per_message
    return tuple(sample(get_all_verbs_from_file(file), verbs_quantity))

