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

        model = ModelDefault(f_name)

        text_module = CursesTextModule()

        view = ViewDefault(model, text_module)

        view_status_bar = ViewStatusBar(text_module)

        clipboard = ClipBoardPyperClip()

        stat_bar_model = StatusBarModel(f_name)

        cursor = CursorCursesDefault(text_module, model)

        deco = ViewDecoratorDefault(view)

        stat_bar_model.registry(view_status_bar)
        stat_bar_model.registry(cursor)
        cursor.registry(view_status_bar)
        cursor.registry(view)
        model.registry(view_status_bar)

        ctrl = ControllerDefault(model, deco, view_status_bar, cursor, stat_bar_model, clipboard)

        app.model = model
        app.view = view
        app.controller = ctrl
        app._view_stat_bar = view_status_bar
        app._view_deco = deco

        return app
