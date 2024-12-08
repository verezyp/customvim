from abc import ABC, abstractmethod
from vimmodules.sides.myvimmodel.appmodel import ModelBase
from vimmodules.sides.myvimview.appview import CursorBase
from vimmodules.sides.myvimmodel.appclipmod import ClipBoardBase

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

    def __init__(self, val: str, model: ModelBase, cursor: CursorBase):
        self._row, self._col = cursor.get_pos()
        self._val = val
        self._model = model
        self._cursor = cursor

    def exec(self):
        self._model.str_sub_sys.insert_str(self._row, self._col, self._val)
        self._cursor.move(self._row, self._col + 1)

    def undo(self):
        pass


class ReplaceDefault(CommandBase):

    def __init__(self, in_chr: chr, cursor: CursorBase, model: ModelBase):
        self._row, self._col = cursor.get_pos()
        self._chr = in_chr
        self._model = model

    def exec(self):
        self._model.str_sub_sys.replace_chr(self._row, self._col, self._chr)

    def undo(self):
        pass


class CutFullDefault(CommandBase):

    def __init__(self, model: ModelBase, cursor: CursorBase, clipboard: ClipBoardBase):
        self._row, _ = cursor.get_pos()
        self._model = model
        self._cursor = cursor
        self._clipboard = clipboard

    def exec(self):
        self._clipboard.copy(self._model.get_str(self._row))
        self._model.str_sub_sys.erase_full_str(self._row)
        # self._model.str_sub_sys.insert_str(self._row, 0, "")

    def undo(self):
        pass


class MakeEmptyDefault(CommandBase):

    def __init__(self, model: ModelBase, cursor: CursorBase):
        self._row, _ = cursor.get_pos()
        self._model = model
        self._cursor = cursor

    def exec(self):
        self._model.str_sub_sys.make_empty(self._row)
        # self._model.str_sub_sys.insert_str(self._row, 0, "")

    def undo(self):
        pass


class EraseCharDefault(CommandBase):

    def __init__(self, model: ModelBase, cursor: CursorBase):
        self._row, self._col = cursor.get_pos()
        self._model = model
        self._cursor = cursor

    def exec(self):
        if self._col == 0:
            if self._row != 1:
                self._row = self._row - 1
                self._col = len(self._model.get_str(self._row)) - 1
        self._model.str_sub_sys.erase_chr(self._row, self._col - 1)
        self._cursor.move(self._row, self._col - 1)

    def undo(self):
        pass


class EraseDiwDefault(CommandBase):

    def __init__(self, cursor: CursorBase, model: ModelBase):
        self._row, self._col = cursor.get_pos()
        self._model = model

    def exec(self):
        self._model.str_sub_sys.erase_word_diw_spec(self._row, self._col)

    def undo(self):
        pass


class CopyStrDefault(CommandBase):
    def __init__(self, cursor: CursorBase, model: ModelBase, clipboard: ClipBoardBase):
        self._row, self._col = cursor.get_pos()
        self._clipboard = clipboard
        self._model = model

    def exec(self):
        self._clipboard.copy(self._model.get_str(self._row))
        # self._model.str_sub_sys.erase_word_diw_spec(self._row, self._col)

    def undo(self):
        pass


class CopyWordCurPosDefault(CommandBase):
    def __init__(self, cursor: CursorBase, model: ModelBase, clipboard: ClipBoardBase):
        self._row, self._col = cursor.get_pos()
        self._clipboard = clipboard
        self._model = model

    def exec(self):
        self._clipboard.copy(self._model.str_sub_sys.get_word_at_index(self._row, self._col))
        # self._model.str_sub_sys.erase_word_diw_spec(self._row, self._col)

    def undo(self):
        pass


class PasteCurPos(CommandBase):
    def __init__(self, cursor: CursorBase, model: ModelBase, clipboard: ClipBoardBase):
        self._row, self._col = cursor.get_pos()
        self._clipboard = clipboard
        self._model = model
        self._cursor = cursor

    def exec(self):
        paste_val = self._clipboard.paste()
        self._model.str_sub_sys.insert_str(self._row, self._col, paste_val)
        self._cursor.move(self._row, len(paste_val) + 1)

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


class SearchStrFromCurTo(CommandBase):  # ...

    def __init__(self, direction: str, text: str, cursor: CursorBase, model: ModelBase):
        self._row, self._col = cursor.get_pos()
        self._text = text
        self._model = model
        self._dir = direction
        self._cursor = cursor

    @property
    def text(self):
        return self._text

    @property
    def direction(self):
        return self._dir

    def exec(self):
        self._row, self._col = self._cursor.get_pos()
        # print(self._row, self._col, self._text, self._dir)
        y, x = self._model.str_sub_sys.find_to(self._row, self._col, self._text, self._dir)
        self._cursor.move(y, x)

    def undo(self):
        pass


'''

CURSOR MOVEMENT

'''


class CursorMoveOneDefault(CommandBase):  # RIGHT LEFT UP DOWN

    def __init__(self, direction: str, cursor: CursorBase):
        self._dir = direction
        self._cursor_inst = cursor

    def exec(self):
        cur_pos_y, cur_pos_x = self._cursor_inst.get_pos()
        match self._dir:
            case "LEFT":
                cur_pos_x -= 1
            case "RIGHT":
                cur_pos_x += 1
            case "UP":
                cur_pos_y -= 1
            case "DOWN":
                cur_pos_y += 1
        self._cursor_inst.move(cur_pos_y, cur_pos_x)

    def undo(self):
        pass


class CursorMoveToStrSideDefault(CommandBase):  # ^ or 0 // $
    def __init__(self, direction: str, cursor: CursorBase, model: ModelBase):
        self._dir = direction
        self._cursor_inst = cursor
        self._model = model

    def exec(self):
        cur_pos_y, cur_pos_x = self._cursor_inst.get_pos()
        match self._dir:
            case "START":
                cur_pos_x = 0
            case "END":
                cur_pos_x = len(self._model.get_str(cur_pos_y)) - 1
        self._cursor_inst.move(cur_pos_y, cur_pos_x)

    def undo(self):
        pass


class CursorMoveWordSideDefault(CommandBase):  # w // b
    def __init__(self, direction: str, cursor: CursorBase, model: ModelBase):
        self._dir = direction
        self._cursor_inst = cursor
        self._model = model

    def exec(self):
        cur_y, cur_x = self._cursor_inst.get_pos()
        match self._dir:
            case "w":
                cur_x = self._model.str_sub_sys.viw_w(cur_y, cur_x)
            case "b":
                cur_x = self._model.str_sub_sys.viw_b(cur_y, cur_x)
        self._cursor_inst.move(cur_y, cur_x)

    def undo(self):
        pass


class CursorMoveToFileStartDefault(CommandBase):
    def __init__(self, cursor: CursorBase, model: ModelBase):
        self._cursor_inst = cursor
        self._model = model

    def exec(self):
        self._cursor_inst.move(0, 0)

    def undo(self):
        pass


class CursorMoveToFileEndDefault(CommandBase):
    def __init__(self, cursor: CursorBase, model: ModelBase):
        self._cursor_inst = cursor
        self._model = model

    def exec(self):
        n = len(self._model.buffer)
        x = len(self._model.get_str(n - 1))
        self._cursor_inst.move(n - 1, x)

    def undo(self):
        pass


class CursorMoveToNDefault(CommandBase):
    def __init__(self, ind: int, cursor: CursorBase, model: ModelBase):
        self._cursor_inst = cursor
        self._model = model
        self._ind = ind

    def exec(self):
        self._cursor_inst.move(self._ind, 0)

    def undo(self):
        pass
