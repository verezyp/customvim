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

    @abstractmethod
    def find(self, in_str: str, index: int):
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

    def find(self, in_str: str, index: int):
        return self._obj.find(in_str, index)


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

    def make_empty(self, row):
        self._base.buffer[row].erase(0, self._base.buffer[row].size() - 1)

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

        for i in range(start_row, edge, shift):
            line = buf[i]
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
        """
        Возвращает слово, на котором находится символ с указанным индексом.

        :param sentence: Строка, содержащая текст.
        :param char_index: Индекс символа в строке.
        :return: Слово, к которому относится символ, или сообщение об ошибке.
        """
        sentence = self._base.get_str(row)
        char_index = col
        # Проверяем, что индекс не выходит за пределы строки
        if char_index < 0 or char_index >= len(sentence):
            return "Индекс вне диапазона строки"

        # Разбиваем строку на слова с их начальным и конечным индексами
        words = sentence.split()
        current_index = 0

        for word in words:
            word_start = current_index
            word_end = current_index + len(word) - 1

            if word_start <= char_index <= word_end:
                return word

            # Учитываем пробел после слова
            current_index += len(word) + 1

        return None


class ModelDefault(ModelBase):
    _file_sub_sys: ModelFileSubSystemBase
    _str_sub_sys: ModelStrSubSystemBase
    _filename: str = None
    _mode: str = None
    _string_handler = None
    _buffer = []

    def __init__(self, filename: str):
        self._filename = filename

        self._file_sub_sys = ModelFileSubSystemDefault()
        self._str_sub_sys = ModelStrSubSystemDefault(self)

        self._buffer = self._file_sub_sys.get_from(filename)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

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

# d = [MyString("3i3i3i3i3i\n"), MyString("ksjsfjjfgsj")]
# m = ModelFileSubSystemDefault()
# m.load_to("file3", d)

# s = MyString("123123TYU93939")
# print(s.find("8"))
# # FIX FIND
