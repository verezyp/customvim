from abc import ABC, abstractmethod
from vimmodules.sides.myvimetc.cursesadapt import *
from vimmodules.sides.myvimmodel.appmodel import *
import os
import ctypes


class CursorBase(ABC):

    @abstractmethod
    def move(self, y, x):
        pass

    @abstractmethod
    def get_pos(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_pos(self, y, x):
        pass


class ViewBase(ABC):

    @abstractmethod
    def display(self):
        pass

    @property
    @abstractmethod
    def text_module(self) -> ITextModule:
        pass

    @property
    @abstractmethod
    def help_state(self):
        pass

    @help_state.setter
    @abstractmethod
    def help_state(self, val):
        pass

    @property
    @abstractmethod
    def cursor(self) -> CursorBase:
        pass


class CursorCursesDefault(CursorBase, ObservableBaseMixin, ObserverBase):

    def __init__(self, text_module_inst: CursesTextModule, model: ModelBase):
        self._inst = text_module_inst
        self._model = model
        self._x = 0
        self._y = 0
        self._buf_link = []
        self._screen_x = 0
        self._screen_y = 0
        self._top_line = 0
        self._set_num = 0
        self._set_num_shift = 6

    def notify(self, arg_dict):
        if 'buffer' in arg_dict:
            self._buf_link = arg_dict["buffer"]
        if 'setnum' in arg_dict:
            self._set_num = arg_dict["setnum"]

    def update(self):
        d = {'cur_y': self._y, 'cur_x': self._x, 'topline': self._top_line}
        for obs in self._obs_list:
            obs.notify(d)

    def get_pos(self):
        return self._y, self._x - self._set_num_shift * self._set_num

    def set_pos(self, y, x):
        self._y, self._x = y, x

    def move(self, y, x):
        len_buf = len(self._model.buffer)
        x = x + self._set_num_shift * self._set_num
        if y < 0 or y > len_buf - 1:
            return None

        len_str = len(self._model.get_str(y)) - 1

        l_edge = 0
        if self._set_num:
            l_edge = self._set_num_shift

        if l_edge > x > 0:
            x = self._set_num_shift
        if x < 0:
            return None

        if x > len_str:
            x = len_str
        self._x = self._x
        self._y = y
        self._x = x
        print(x)
        if y < self._top_line:
            self._top_line = y
        elif y >= self._top_line + 28:
            self._top_line = y - 27
        # self.update()
        self._screen_y = y - self._top_line

        # self._scaling()
        # print(self._screen_y, y, self._top_line)
        self._inst.cursor_move(self._screen_y, x)

        self.update()


from vimmodules.sides.myvimmodel.appmodel import ObserverBase


class ViewStatusBar(ViewBase, ObserverBase):  # subs to StatBarModel, CursorModel, CoreModel

    _buf = [None, "pp", 0, 0, None]

    def __init__(self, text_mod: ITextModule):
        self._text_module = text_mod
        self._win = curses.newwin(1, 120, 30 - 1, 0)
        self.screen_configure()

    @property
    def help_state(self):
        return None

    def notify(self, arg_dict: dict):
        if 'filename' in arg_dict:
            self._buf[0] = arg_dict["filename"]
        if 'mode' in arg_dict:
            self._buf[1] = arg_dict["mode"]
        if 'cur_y' in arg_dict:
            self._buf[2] = arg_dict["cur_y"]
        if 'amount' in arg_dict:
            self._buf[3] = arg_dict["amount"]
        if 'tmp_str' in arg_dict:
            self._buf[4] = arg_dict["tmp_str"]
        self.display()

    @staticmethod
    def _set_console_size(width, height):
        os.system(f"mode con: cols={width} lines={height}")

        hwnd = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

        rect = ctypes.create_string_buffer(22)
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(hwnd, rect)

        left, top, right, bottom = 0, 0, width - 1, height - 1

        ctypes.windll.kernel32.SetConsoleWindowInfo(hwnd, True, ctypes.byref(
            (ctypes.c_short * 4)(left, top, right, bottom)
        ))

    def screen_configure(self):
        screen = self._text_module
        # self._set_console_size(120, 30)
        # screen.noecho()  # Отключаем отображение вводимых символов
        # screen.cbreak()  # Оперативное получение символов без ожидания Enter
        # screen.keypad(True)  # Включаем обработку специальных клавиш (стрелок)
        # screen.set_cursor(1)  # Включаем отображение курсора

    def display(self):
        stdscr = self._text_module
        # stdscr.clear_scr()
        self._win.clear()
        file = self._buf[0]
        mode = self._buf[1]
        cursor_y = self._buf[2]
        amount = self._buf[3]
        max_y, max_x = 30, 120

        if self._buf[4] == "":
            status_bar = f"FILE: {file}. MODE: {mode}. CUR_STR: {cursor_y}. AMOUNT: {amount}."
        else:
            status_bar = f"FILE: {file}. MODE: {mode}. CUR_STR: {cursor_y}. AMOUNT: {amount}. |{self._buf[4]}"

        self._win.refresh()
        self._win.addstr(0, 0, status_bar[:max_x - 1])
        self._win.refresh()

    @property
    def text_module(self) -> ITextModule:
        pass

    @property
    def cursor(self) -> CursorBase:
        pass


class ViewDecoratorBase(ViewBase):
    def display(self):
        pass

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val

    @property
    def text_module(self) -> ITextModule:
        return self.component.text_module

    @property
    def help_state(self):
        return self.component.help_state

    @help_state.setter
    def help_state(self, val):
        self.component.help_state = val

    @property
    def cursor(self) -> CursorBase:
        return self.component.cursor

    _component: ViewBase = None

    def __init__(self, component: ViewBase) -> None:
        self._component = component
        self._state = 0

    @property
    def component(self) -> ViewBase:
        return self._component


class ViewDecoratorDefault(ViewDecoratorBase, ObserverBase):
    def notify(self, *args, **kwargs):
        return self.component.notify(*args, **kwargs)

    def display(self):
        m = self.component.display()
        module = self.component.text_module
        if self.state == 0:
            return []

        stdscr = self.component.text_module
        max_y, max_x = stdscr.getmaxyx()
        win2 = module.newwin(max_y - 1, max_x - 1, 0, 0)
        module.start_color()
        module.init_pair(1, "RED", "BLACK")
        module.init_pair(2, "WHITE", "BLACK")
        keywords = {"def", "class", "for", "in", "while", "if", "elif", "else", "raise", "async", "match", "pass",
                    "continue", "yield", "break", "import", "from"}
        for i, line in enumerate(m):
            x = 0
            word = ""
            for char in line:
                if char.isspace() or char == ":":
                    if word in keywords:
                        module.win_addstr(i, x - len(word), word, win2, 1)
                    else:
                        module.win_addstr(i, x - len(word), word, win2, 2)
                    word = ""
                    module.win_addstr(i, x, char, win2)
                    x += 1
                else:
                    word += char
                    module.win_addstr(i, x, char, win2)
                    x += 1

            if word in keywords:
                module.win_addstr(i, x - len(word), word, win2, 1)
            else:
                module.win_addstr(i, x - len(word), word, win2, 2)
        module.win_refresh(win2)


class ViewDefault(ViewBase, ObserverBase):
    _cursor_inst: CursorBase
    _text_module: ITextModule
    _model_inst: ModelBase
    _scr_top_str: int = 0
    _scr_bot_str: int = 29

    def __init__(self, model: ModelBase, text_mod: ITextModule):
        mod = CursesTextModule()
        self._text_module = text_mod
        self._model_inst = model
        self._set_console_size(120, 30)
        self.screen_configure()
        self._cursor_inst = CursorCursesDefault(mod, model)
        self._cursor_x = 0
        self._cursor_y = 0
        self._top = 0
        self._help_state = 0
        self._set_num = 0

    @property
    def help_state(self):
        return self._help_state

    @help_state.setter
    def help_state(self, val):
        self._help_state = val

    def notify(self, args_dict):
        if "cur_x" in args_dict:
            self._cursor_x = args_dict["cur_x"]
        if "cur_y" in args_dict:
            self._cursor_y = args_dict["cur_y"]
        if "topline" in args_dict:
            self._top = args_dict["topline"]
        if "setnum" in args_dict:
            self._set_num = args_dict["setnum"]

    @property
    def text_module(self):
        return self._text_module

    @property
    def cursor(self) -> CursorBase:
        return self._cursor_inst

    def screen_configure(self):
        screen = self._text_module
        screen.noecho()  # Отключаем отображение вводимых символов
        screen.cbreak()  # Оперативное получение символов без ожидания Enter
        screen.keypad(True)  # Включаем обработку специальных клавиш (стрелок)
        screen.set_cursor(1)  # Включаем отображение курсора

    def set_edges(self, top_val: int, bot_val: int):
        self._scr_top_str, self._scr_bot_str = top_val, bot_val

    @staticmethod
    def _set_console_size(width, height):
        os.system(f"mode con: cols={width} lines={height}")

        hwnd = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

        rect = ctypes.create_string_buffer(22)
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(hwnd, rect)

        left, top, right, bottom = 0, 0, width - 1, height - 1

        ctypes.windll.kernel32.SetConsoleWindowInfo(hwnd, True, ctypes.byref(
            (ctypes.c_short * 4)(left, top, right, bottom)
        ))

    def display(self):  # 0 - 28 string + last - status_bar (set_console_size(120, 30))
        stdscr = self._text_module
        max_y, max_x = stdscr.getmaxyx()
        win2 = self._text_module.newwin(max_y - 1, max_x - 1, 0, 0)
        top_line = self._top
        main_text = []
        help_buffer = ["i Ввод текста перед курсором",
                       "I Перейти в начало строки и начать ввод текста",
                       "A Перейти в конец строки и начать ввод текста",
                       "S Удалить содержимое строки и начать ввод текста",
                       "r Заменить один символ под курсором",
                       "^/0 Перемещение курсора в начало строки",
                       "$ Перемещение курсора в конец строки",
                       "w Перемещение курсора в конец слова справа от курсора ",
                       "b Перемещение курсора в начало слова слева от курсора ",
                       "gg Перейти в начало файла",
                       "G Перейти в конец файла",
                       "NG Перейти на строку с номером N",
                       "PG_UP Перейти на экран вверх",
                       "PG_DOWN Перейти на экран вниз",
                       "x Заменить один символ под курсором",
                       "diw Удалить слово под курсором, включая пробел справа",
                       "dd Вырезать текущую строку",
                       "yy Копировать текущую строку",
                       "yw Копировать слово под курсором",
                       "p Вставить после курсора",
                       "/text Поиск строки text от курсора до конца файла",
                       "?text Поиск строки text от курсора до начала файла",
                       "n Повторить поиск",
                       "N Повторить поиск в обратном направлении"
                       ]
        n = 28
        if len(self._model_inst.buffer) < 28:
            n = len(self._model_inst.buffer)
        if self._help_state == 0:
            for i in range(top_line, top_line + n):
                main_text.append(self._model_inst.get_str(i))
        else:
            main_text = help_buffer
        self._text_module.win_clear(win2)
        # win2.clear()
        i = 0
        mas = []
        for line in main_text:
            if self._set_num:
                self._text_module.win_addstr(i, 0,
                                             str(i + top_line) + ((i + top_line) < 10) * " " + (
                                                     (i + top_line) < 100) * " "
                                             + ((i + top_line) < 1000) * " " + (
                                                     (i + top_line) < 10000) * " " + " " + line, win2)
                mas.append(str(i + top_line) + ((i + top_line) < 10) * " " + ((i + top_line) < 100) * " "
                           + ((i + top_line) < 1000) * " " + ((i + top_line) < 10000) * " " + " " + line)
            else:
                mas.append(line)
                self._text_module.win_addstr(i, 0, line, win2)
                # win2.addstr(i, 0, line)
            i += 1
        self._text_module.win_refresh(win2)
        # win2.refresh()
        return mas
