from vimmodules.sides.myvimview.appview import ViewStatusBar
from vimmodules.sides.myvimetc.cursesadapt import CursesTextModule
from vimmodules.apphandler import AppHandler


class One:
    __buf = [1, 2, 3, 4]

    @property
    def buffer(self):
        print("1 addr ", id(self.__buf))
        return self.__buf


class Two:
    _buf2 = []

    def __init__(self, obj: One):
        self._obj = obj
        self._buf2 = obj.buffer

    def m1(self):
        print("2 addr ", id(self._buf2))
        return self._buf2

    def m2(self):
        self._buf2[0] = 999


import os
import ctypes


def set_console_size(width, height):
    os.system(f"mode con: cols={width} lines={height}")

    hwnd = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

    rect = ctypes.create_string_buffer(22)
    ctypes.windll.kernel32.GetConsoleScreenBufferInfo(hwnd, rect)

    left, top, right, bottom = 0, 0, width - 1, height - 1

    ctypes.windll.kernel32.SetConsoleWindowInfo(hwnd, True, ctypes.byref(
        (ctypes.c_short * 4)(left, top, right, bottom)
    ))


from vimmodules.sides.myvimmodel.appmodel import ModelDefault


def config1():
    m = ModelDefault("file3")
    l = len(m.buffer)
    for i in range(l):
        print(f"{i})", m.get_str(i))
    m.str_sub_sys.insert_str(0, len(m.get_str(0)) - 1, m.get_str(1))
    l = len(m.buffer)
    for i in range(l):
        print(f"{i})", m.get_str(i))


if __name__ == "__main__":
    # config1()
    # c1 = One()
    # c2 = Two(c1)
    # print(c1.buffer)
    # print(c2.m1())
    # c2.m2()
    # print(c2.m1())
    # print(c1.buffer)
    # set_console_size(120, 30)
    # s = "12345\n"
    # print(s[2:])
    # exit()
    AppHandler().start()
