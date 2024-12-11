from vimmodules.sides.myvimcontroller.appcontroller import *
from vimmodules.sides.myvimmodel.appmodel import *
from vimmodules.sides.myvimcontroller.appcommands import *


class AppBase(ABC):

    @property
    @abstractmethod
    def view(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass

    @property
    @abstractmethod
    def controller(self):
        pass

    @property
    @abstractmethod
    def filename(self):
        pass

    @abstractmethod
    def run(self):
        pass


class AppBuilderBase(ABC):
    @abstractmethod
    def set_view(self, inst):
        pass

    @abstractmethod
    def set_controller(self, inst):
        pass

    @abstractmethod
    def set_model(self, inst):
        pass

    @abstractmethod
    def create(self, f_name) -> AppBase:
        pass


class AppDefault(AppBase):

    def __init__(self):
        self._model = None
        self._view = None
        self._controller = None
        self._filename = None
        self._view_stat_bar = None
        self._view_deco = None
        # v =

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, f_name):
        self._filename = f_name

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, inst):
        self._view = inst

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, inst):
        self._model = inst

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, inst):
        self._controller = inst

    def run(self):
        d = ViewDecoratorDefault(self._view)
        while True:
            self._view_deco.display()
            self._view_stat_bar.display()
            self.controller.process()


class AppBuilderDefault(AppBuilderBase):

    def set_view(self, inst):
        pass

    def set_controller(self, inst):
        pass

    def set_model(self, inst):
        pass

    def create(self, f_name):
        app = AppDefault()
        v = ViewStatusBar(CursesTextModule())
        app.model = ModelDefault(f_name)
        app.view = ViewDefault(app.model)
        app._view_stat_bar = v
        app._view_deco = ViewDecoratorDefault(app.view)
        app.controller = ControllerDefault(app.model, app._view_deco, v)
        return app
