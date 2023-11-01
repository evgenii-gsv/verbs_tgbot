class FileWithVerbsNotFound(Exception):
    """No file containing irregular verbs found"""

class InvalidAnswer(Exception):
    """The answer is invalid"""

class NotSameLength(InvalidAnswer):
    """The answers' quantity is not the same as the questions' quantity"""
