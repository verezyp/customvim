from trymodel import *
from vimmodules.sides.myvimetc.cursesadapt import *


class TryView:
    _filename: str = None
    _model_instance: TryModel
    _interface_instance: ITextModule

    def __init__(self, model_inst, iface_inst: ITextModule):
        self._model_instance = model_inst
        self._interface_instance = iface_inst
        self._interface_instance.clear_scr()

    def display_str(self, number):
        self._interface_instance.add_str(number, 0, self._model_instance.get_cur_string(number))

    def display_screen(self, amount=20):
        for i in range(1, amount):
            self.display_str(i)
