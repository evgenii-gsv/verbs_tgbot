from pathlib import Path
from typing import ClassVar, List, Tuple, Type
from random import sample
from marshmallow_dataclass import dataclass
from marshmallow import Schema

from verbs_tgbot.config_reader import config
from verbs_tgbot.services.exceptions import FileWithVerbsNotFound


@dataclass(frozen=True)
class IrregularVerb:
    """A dataclass to store information about an irregular verb."""
    
    first_form: str
    second_form: str
    third_form: str
    Schema: ClassVar[Type[Schema]] = Schema # type: ignore

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

# lst = IrregularVerb('be', 'was', 'been'), IrregularVerb('have', 'had', 'had')
# j = IrregularVerb.Schema().dump(lst, many=True)
# print(j)
# v: List[IrregularVerb] = IrregularVerb.Schema().load(j, many=True)
# print(v[0])