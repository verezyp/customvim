from abc import ABC, abstractmethod
from typing import overload

from vimmodules.sides.myvimetc.MyString import MyString
from vimmodules.sides.myvimetc.observer import *


class IStringHandler(ABC):

    @abstractmethod
    def data(self) -> str:  # MyString ???
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass

    @abstractmethod
    def insert(self, in_str, ind):
        pass

    @abstractmethod
    def replace(self, index: int, count: int, in_str: str):
        pass

    @abstractmethod
    def erase(self, index, count):
        pass

    @abstractmethod
    def find(self, in_str: str, index: int):
        pass


class MyStringHandler(IStringHandler):

    # overload ???
    def __init__(self, init_str: str = None, count_of_symbols: int = None, symbol: chr = None):
        self._obj = None
        if not (init_str is None) and count_of_symbols is None and symbol is None:
            self._obj = MyString(init_str)
        elif not (init_str is None) and not (count_of_symbols is None):
            self._obj = MyString(init_str, count_of_symbols)
        elif not (count_of_symbols is None) and not (symbol is None):
            self._obj = MyString(count_of_symbols, symbol)
        elif all((init_str is None, count_of_symbols is None, symbol is None)):
            self._obj = MyString()
        else:
            raise Exception(AttributeError)

    def data(self) -> str:
        return self._obj.data()

    def size(self) -> int:
        return self._obj.size()

    def empty(self) -> bool:
        return self._obj.empty()

    def insert(self, in_str, ind):
        return self._obj.insert(ind, in_str)

    def replace(self, index: int, count: int, in_str: str):
        return self._obj.replace(index, count, in_str)

    def erase(self, index, count):
        return self._obj.erase(index, count)

    def find(self, in_str: str, index: int):
        return self._obj.find(in_str, index)


class DefaultStringHandler(IStringHandler):

    def __init__(self, string: str):
        self._obj = string

    def data(self) -> str:
        return self._obj

    def size(self) -> int:
        return len(self._obj)

    def empty(self) -> bool:
        return self._obj == ""

    def insert(self, in_str: str, ind):
        s_list = list(self._obj)
        s_list.insert(ind, in_str)
        self._obj = ''.join(s_list)

    def replace(self, index: int, count: int, in_str: str):
        new_str = self._obj[:index] + in_str + self._obj[index + count:]
        self._obj = new_str

    def erase(self, index, count):
        self.replace(index, count, "")

    def find(self, in_str: str, index: int):
        return self._obj.find(in_str, index)


class ModelFileSubSystemBase(ABC):

    @abstractmethod
    def get_from(self, filename: str, *args, **kwargs):
        pass

    @abstractmethod
    def load_to(self, filename: str, buf):
        pass


class ModelStrSubSystemBase(ABC):
    @abstractmethod
    def insert_str(self, row: int, col: int, input_str: str):
        pass

    @abstractmethod
    def insert_new(self, row: int, col: int, input_str: str):
        pass

    @abstractmethod
    def replace_chr(self, row, col, input_chr: chr):
        pass

    @abstractmethod
    def erase_full_str(self, row: int) -> None:
        pass

    @abstractmethod
    def make_empty(self, row):
        pass

    @abstractmethod
    def erase_chr(self, row: int, col: int) -> None:
        pass

    @abstractmethod
    def erase_word_diw_spec(self, row: int, col) -> None:
        pass

    @abstractmethod
    def find_to(self, *args, **kwargs):
        pass

    @abstractmethod
    def viw_w(self, cur_y: int, cur_x: int) -> int:
        pass

    @abstractmethod
    def viw_b(self, cur_y: int, cur_x: int) -> int:
        pass

    @abstractmethod
    def get_word_at_index(self, row: int, col: int) -> str:
        pass


class ModelBase(ABC):
    @property
    @abstractmethod
    def filename(self):
        pass

    @abstractmethod
    def cancel_all(self):
        pass

    @property
    @abstractmethod
    def buffer(self):
        pass

    @filename.setter
    @abstractmethod
    def filename(self, value):
        pass

    @property
    @abstractmethod
    def edited(self):
        pass

    @edited.setter
    @abstractmethod
    def edited(self, val):
        pass

    @abstractmethod
    def get_str(self, num: int):
        pass

    @buffer.setter
    @abstractmethod
    def buffer(self, value):
        pass

    @property
    @abstractmethod
    def str_sub_sys(self) -> ModelStrSubSystemBase:
        pass

    @property
    @abstractmethod
    def file_sub_sys(self) -> ModelFileSubSystemBase:
        pass

    @property
    @abstractmethod
    def mode(self):
        pass

    @mode.setter
    def mode(self, val):
        pass


class ModelFileSubSystemDefault(ModelFileSubSystemBase):
    _str_handler: IStringHandler = MyStringHandler

    def get_from(self, filename: str, model: ModelBase):
        buf = []
        bp = []
        if filename is None:
            return None
        with open(filename, "r") as f:
            while True:
                line = f.readline()
                # line = line.replace('\n', '')
                ms_line = self._str_handler(line)
                bp_line = self._str_handler(line)
                if not line:
                    break
                buf.append(ms_line)
                bp.append(bp_line)
            model.buffer = buf
            model._backup = bp
            return buf

    def load_to(self, filename, buf):
        f = open(filename, "w")
        [f.write(line.data()) for line in buf]


class ModelStrSubSystemDefault(ModelStrSubSystemBase):

    def __init__(self, base: ModelBase):
        self._base = base
        self._string_handler = MyStringHandler

    def insert_new(self, row: int, col: int, input_str: str):
        s = self._string_handler(self._base.get_str(row)[col:])
        self._base.buffer[row].erase(col, len(self._base.buffer[row].data()) - col - 1)
        self._base.buffer.insert(row + 1, s)
        self._base.edited = True

    def insert_str(self, row: int, col: int, input_str: str) -> None:
        self._base.buffer[row].insert(input_str, col)
        self._base.edited = True

    def replace_chr(self, row, col, input_chr: chr) -> None:
        self._base.buffer[row].replace(col, 1, input_chr)
        self._base.edited = True

    def erase_full_str(self, row: int) -> None:
        self._base.buffer.pop(row)
        self._base.edited = True

    def make_empty(self, row):
        if self._base.buffer[row].size() > 1:
            self._base.buffer[row].erase(0, self._base.buffer[row].size() - 1)
        self._base.edited = True

    def erase_chr(self, row: int, col: int) -> None:
        self._base.buffer[row].erase(col, 1)
        self._base.edited = True

    # TEST IT
    def erase_word_diw_spec(self, row: int, col) -> None:
        s = self._base.buffer[row]
        sdata = s.data()
        left_ind = col
        right_ind = col
        while True:
            symb = sdata[left_ind]
            if symb != ' ' and symb != '\n' and left_ind != 0:
                left_ind -= 1
            else:
                break
        while True:
            symb = sdata[right_ind]
            if symb != ' ' and symb != '\n' and right_ind != len(sdata):
                right_ind += 1
            else:
                break

        dif = right_ind - left_ind
        s.erase(left_ind, dif)
        self._base.buffer[row] = s
        self._base.edited = True

    def get_end_of_str(self, row: int) -> int:
        return self._base.buffer[row].size() - 1

    def find_to(self, start_row: int, start_col: int, in_str: str, direction: str) -> tuple[int, int]:
        buf = self._base.buffer
        ind = -1
        line_number = -1

        edge = len(buf)
        shift = 1

        if direction == "TOP":
            edge = 0
            shift = -1

        for i in range(start_row, edge + shift - 1, shift):
            line = buf[i]
            print(i)
            if i == start_row:
                ind = line.find(in_str, start_col)
            else:
                ind = line.find(in_str, 0)

            if not (ind == -1):
                line_number = i
                break

        return line_number, ind

    def viw_w(self, cur_y: int, cur_x: int) -> int:
        index = cur_x
        text = self._base.get_str(cur_y)

        n = len(text)
        if index >= n - 1:
            return n

        while index < n and text[index].isalnum():
            index += 1

        while index < n and not text[index].isalnum():
            index += 1
        return index

    def viw_b(self, cur_y: int, cur_x: int) -> int:
        index = cur_x
        text = self._base.get_str(cur_y)

        if index <= 0:
            return 0

        index -= 1
        while index > 0 and not text[index].isalnum():
            index -= 1

        while index > 0 and text[index - 1].isalnum():
            index -= 1
        return index

    def get_word_at_index(self, row: int, col: int):

        sentence = self._base.get_str(row)
        char_index = col
        if char_index < 0 or char_index >= len(sentence):
            raise IndexError

        words = sentence.split()
        current_index = 0

        for word in words:
            word_start = current_index
            word_end = current_index + len(word) - 1

            if word_start <= char_index <= word_end:
                return word

            current_index += len(word) + 1

        return None


class ObservableBaseMixin(ObservableBase):
    _obs_list: list[ObserverBase] = []

    def registry(self, obj: ObserverBase):
        self._obs_list.append(obj)
        self.update()

    def unsubscribe(self, obj: ObserverBase):
        self._obs_list.remove(obj)

    @abstractmethod
    def update(self, *args, **kwargs):
        for obs in self._obs_list:
            obs.notify()


class ModelDefault(ModelBase, ObservableBaseMixin):
    _file_sub_sys: ModelFileSubSystemBase
    _str_sub_sys: ModelStrSubSystemBase
    _filename: str = None
    _mode: str = None
    _string_handler = None
    _buffer = []
    _edited: bool = False
    _backup = []

    def __init__(self, filename: str):
        self._filename = filename

        self._file_sub_sys = ModelFileSubSystemDefault()
        self._str_sub_sys = ModelStrSubSystemDefault(self)

        self._buffer = self._file_sub_sys.get_from(filename, self)

    def update(self):
        d = {'amount': len(self._buffer), 'buffer': self.buffer}
        for obs in self._obs_list:
            obs.notify(d)

    @staticmethod
    def upd(func):
        def wrapper(self, *args, **kwargs):
            f = func(self, *args, **kwargs)
            self.update()
            return f

        return wrapper

    def cancel_all(self):
        self._buffer = self._backup.copy()
        self.update()

    @property
    @upd
    def edited(self):
        return self._edited

    @edited.setter
    def edited(self, val):
        self._edited = val

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

    @property
    @upd
    def str_sub_sys(self):
        return self._str_sub_sys

    @property
    @upd
    def file_sub_sys(self):
        return self._file_sub_sys

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, val):
        self._filename = val

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, val):
        self._buffer = val

    def get_str(self, num: int):
        return self._buffer[num].data()


class StatusBarModel(ObservableBaseMixin, ObserverBase):
    _filename: str = None
    _mode: str = "NAVI"
    _tmp_str: str = ""
    _set_num: int = 0

    def __init__(self, file):
        super().__init__()
        self._filename = file

    def update(self):
        d = {"filename": self._filename, "mode": self._mode, "tmp_str": self._tmp_str, "setnum": self._set_num}
        for obs in self._obs_list:
            obs.notify(d)

    def notify(self, *args, **kwargs):
        pass

    @property
    def set_num(self):
        return self._set_num

    @set_num.setter
    def set_num(self, val):
        self._set_num = val

    def registry(self, obj: ObserverBase):
        super().registry(obj)
        self.update()

    @property
    def tmp_str(self):
        return self._tmp_str

    @tmp_str.setter
    def tmp_str(self, val):
        self._tmp_str = val
        self.update()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, file):
        self._filename = file
        self.update()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val: str):
        self._mode = val
        self.update()
