from abc import ABC, abstractmethod
from appdef import *
from appparser import *


class AppHandlerBase(ABC):

    @abstractmethod
    def start(self):
        pass


class AppHandler(AppHandlerBase):
    _builder: AppBuilderBase
    _parser: ArgsParserDefault

    def __init__(self):
        self._builder = AppBuilderDefault()
        self._parser = ArgsParserDefault()

    def start(self):
        app = self._builder.create(self._parser.get_filename())

        app.run()
