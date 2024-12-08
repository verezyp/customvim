from abc import abstractmethod, ABC


class A1(ABC):

    @abstractmethod
    def f1(self):
        pass

    @abstractmethod
    def f2(self):
        pass


class A2(ABC):
    @abstractmethod
    def f1(self):
        pass


class B1(A1, A2):
    def f1(self):
        print("f1")

    def f2(self):
        print("f2")


def p1(obj: A1):
    obj.f1()


if __name__ == '__main__':
    p1(B1())
