from abc import ABC, abstractmethod


class Person(ABC):

    @abstractmethod
    def get_details(self):
        pass


class Student(Person):

    def __init__(self, student_id, name, age):
        self.__student_id = student_id      
        self.__name = name
        self.__age = age

    def get_id(self):
        return self.__student_id

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    def get_details(self):
        return {
            "id": self.__student_id,
            "name": self.__name,
            "age": self.__age
        }