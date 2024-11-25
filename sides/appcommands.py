from abc import ABC, abstractmethod
from appmodel import ModelBase

'''

MODEL COMMANDS

'''


class CommandBase(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def exec(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class InsertDefault(CommandBase):

    def __init__(self, row: int, col: int, val: str, model: ModelBase):
        self._row = row
        self._col = col
        self._val = val
        self._model = model

    def exec(self):
        self._model.str_sub_sys.insert_str(self._row, self._col, self._val)

    def undo(self):
        pass


class ReplaceDefault(CommandBase):

    def __init__(self, row: int, col: int, in_chr: chr, model: ModelBase):
        self._row = row
        self._col = col
        self._chr = in_chr
        self._model = model

    def exec(self):
        self._model.str_sub_sys.replace_chr(self._row, self._col, self._chr)

    def undo(self):
        pass


class EraseFullDefault(CommandBase):

    def __init__(self, row: int, model: ModelBase):
        self._row = row
        self._model = model

    def exec(self):
        self._model.str_sub_sys.erase_full_str(self._row)

    def undo(self):
        pass


class EraseCharDefault(CommandBase):

    def __init__(self, row: int, col: int, model: ModelBase):
        self._row = row
        self._col = col
        self._model = model

    def exec(self):
        self._model.str_sub_sys.erase_chr(self._row, self._col)

    def undo(self):
        pass


class EraseDiwDefault(CommandBase):

    def __init__(self, row: int, col: int, model: ModelBase):
        self._row = row
        self._col = col
        self._model = model

    def exec(self):
        self._model.str_sub_sys.erase_word_diw_spec(self._row, self._col)

    def undo(self):
        pass


class LoadToFileDefault(CommandBase):
    def __init__(self, filename: str, model: ModelBase):
        self._filename = filename
        self._model = model

    def exec(self):
        self._model.file_sub_sys.load_to(self._filename, self._model.buffer)

    def undo(self):
        pass


class SearchStrFromCurToBot(CommandBase):  # ...

    def __init__(self, row: int, col: int, text: str, model: ModelBase):
        self._row = row
        self._col = col
        self._text = text
        self._model = model

    def exec(self):
        pass

    def undo(self):
        pass


'''



'''


class CursorMoveOneDefault(CommandBase):

    def __init__(self, direction: str, cursor):
        pass

    def exec(self):
        pass

    def undo(self):
        pass
