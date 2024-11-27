from abc import ABC, abstractmethod
from sides.appcontroller import ControllerDefault
from sides.appmodel import ModelDefault
from sides.appview import ViewDefault
from sides import *
from sides.cursesadapt import *
from sides.appview import *
from sides.appcontroller import *
from sides.appmodel import *
from sides.appcommands import *


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
            self._view.display()

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

        app.model = ModelDefault(f_name)
        app.view = ViewDefault(app.model)
        app.controller = ControllerDefault(app.model, app.view)
        return app
