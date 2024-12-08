from abc import ABC, abstractmethod


class ObserverBase(ABC):

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass


class ObservableBase(ABC):
    @abstractmethod
    def registry(self, obj):
        pass

    @abstractmethod
    def unsubscribe(self, obj):
        pass

    @abstractmethod
    def update(self):
        pass
