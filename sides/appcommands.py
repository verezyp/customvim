from abc import ABC, abstractmethod
from appmodel import ModelBase


class CommandBase(ABC):

    @abstractmethod
    def exec(self, *args, **kwargs):
        pass

    @abstractmethod
    def undo(self):
        pass


class InsertDefault(CommandBase):

    def exec(self, row: int, col: int, val: str, model: ModelBase):
        model.str_sub_sys.insert_str(row, col, val)

    def undo(self):
        pass


class ReplaceDefault(CommandBase):

    def exec(self, row: int, col: int, in_chr: chr, model: ModelBase):
        model.str_sub_sys.replace_chr(row, col, in_chr)

    def undo(self):
        pass


class EraseFullDefault(CommandBase):
    def exec(self, row: int, model: ModelBase):
        model.str_sub_sys.erase_full_str(row)

    def undo(self):
        pass


class EraseCharDefault(CommandBase):
    def exec(self, row: int, col: int, model: ModelBase):
        model.str_sub_sys.erase_chr(row, col)

    def undo(self):
        pass


class EraseDiwDefault(CommandBase):
    def exec(self, row: int, col: int, model: ModelBase):
        model.str_sub_sys.erase_word_diw_spec(row, col)

    def undo(self):
        pass




class LoadToFileDefault(CommandBase):
    def exec(self, filename: str, model: ModelBase):
        model.file_sub_sys.load_to(filename, model.buffer)

    def undo(self):
        pass
