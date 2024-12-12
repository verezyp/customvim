from abc import ABC, abstractmethod
from vimmodules.sides.myvimetc.cursesadapt import *
from vimmodules.sides.myvimetc.observer import ObserverBase
from vimmodules.sides.myvimmodel.appmodel import ModelBase, ObservableBaseMixin


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

    def get_pos2(self):
        return self._y, self._x - 2 * self._set_num

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
