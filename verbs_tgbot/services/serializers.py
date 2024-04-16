from typing import List, Sequence

from verbs_tgbot.services.irregular_verbs import IrregularVerb


def serialize_verbs(data: Sequence[IrregularVerb]) -> Sequence[dict]:
    return IrregularVerb.Schema().dump(data, many=True)


def deserialize_verbs(data: Sequence[dict]) -> List[IrregularVerb]:
    return IrregularVerb.Schema().load(data, many=True)
