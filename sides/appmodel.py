from abc import ABC, abstractmethod
from MyString import MyString


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


class MyStringHandler(IStringHandler):
    _obj = None

    # overload ???
    def __init__(self, init_str: str = None, count_of_symbols: int = None, symbol: chr = None):
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


class ModelFileSubSystemBase(ABC):

    @abstractmethod
    def get_from(self, filename: str):
        pass

    @abstractmethod
    def load_to(self, filename: str, buf):
        pass


class ModelStrSubSystemBase(ABC):
    @abstractmethod
    def insert_str(self, row: int, col: int, input_str: str):
        pass

    @abstractmethod
    def replace_chr(self, row, col, input_chr: chr):
        pass

    @abstractmethod
    def erase_full_str(self, row: int) -> None:
        pass

    @abstractmethod
    def erase_chr(self, row: int, col: int) -> None:
        pass

    @abstractmethod
    def erase_word_diw_spec(self, row: int, col) -> None:
        pass


class ModelBase(ABC):
    @property
    @abstractmethod
    def filename(self):
        pass

    @property
    @abstractmethod
    def buffer(self):
        pass

    @filename.setter
    @abstractmethod
    def filename(self, value):
        pass

    @abstractmethod
    def get_str(self, num: int):
        pass

    @abstractmethod
    def get_statusbar_info(self):
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


class ModelFileSubSystemDefault(ModelFileSubSystemBase):
    _str_handler: IStringHandler = MyStringHandler

    def get_from(self, filename):
        buf = []
        if filename is None:
            return None
        with open(filename, "r") as f:
            while True:
                line = f.readline()
                ms_line = self._str_handler(line)
                if not line:
                    break
                buf.append(ms_line)
            return buf

    def load_to(self, filename, buf):
        f = open(filename, "w")
        [f.write(line.data()) for line in buf]


class ModelStrSubSystemDefault(ModelStrSubSystemBase):

    def __init__(self, base: ModelBase):
        self._base = base

    def insert_str(self, row: int, col: int, input_str: str) -> None:
        self._base.buffer[row].insert(input_str, col)

    def replace_chr(self, row, col, input_chr: chr) -> None:
        self._base.buffer[row].replace(col, 1, input_chr)

    def erase_full_str(self, row: int) -> None:
        self._base.buffer.pop(row)

    def erase_chr(self, row: int, col: int) -> None:
        self._base.buffer[row].erase(col, 1)

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

        dif = right_ind - left_ind + 1
        s.erase(left_ind, dif)
        self._base.buffer[row] = s


class ModelDefault(ModelBase):
    _file_sub_sys: ModelFileSubSystemBase
    _str_sub_sys: ModelStrSubSystemDefault
    _filename: str = None
    _mode: str = None
    _string_handler = None
    _buffer = []

    def __init__(self, filename: str):
        self._filename = filename

        self._file_sub_sys = ModelFileSubSystemDefault()
        self._str_sub_sys = ModelStrSubSystemDefault(self)

        self._buffer = self._file_sub_sys.get_from(filename)

    def tmpmet(self):
        [print(t.data()) for t in self._buffer]
        self._str_sub_sys.erase_word_diw_spec(1, 3)
        [print(t.data()) for t in self._buffer]

    @property
    def str_sub_sys(self):
        return self._str_sub_sys

    @property
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

    def get_statusbar_info(self):
        pass


# d = [MyString("3i3i3i3i3i\n"), MyString("ksjsfjjfgsj")]
# m = ModelFileSubSystemDefault()
# m.load_to("file3", d)
m = ModelDefault("file3")
