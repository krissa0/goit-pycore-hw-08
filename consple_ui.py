from abc import ABC, abstractmethod

class Console(ABC): # Абстрактний класс для виведення інформації користувачу
    @abstractmethod
    def show_message(self, message):
        pass

    @abstractmethod
    def show_result(self, result):
        pass

class Console2(Console):
    def show_message(self, message):
        print(message) # Виводимо смс користувачу

    def show_result(self, result):
        print(result) # Виводимо результат користувачу