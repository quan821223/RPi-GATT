#p1_2.py
from abc import ABCMeta, abstractmethod
# 引入ABCMeta和abstractmethod來定義抽象類別和抽象方法


class Register(metaclass=ABCMeta):
    """觀察者的基類別"""
    @abstractmethod
    def update(self, observable, object):
        pass


class UnRegister:
    """被觀察者的基類別"""
    def __init__(self):
        self.__observersList = []

    # private
    def addObserver(self, register):
        self.__observersList.append(register)

    # private
    def removeObserver(self, register):
        self.__observersList.remove(register)

    # notify
    def notifyObservers(self, object=0):
        for o in self.__observersList:
            o.update(self, object)

