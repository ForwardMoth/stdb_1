import sys

sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.people_table import *
from tables.phones_table import *

class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        self.person_id = None
        self.person_obj = None
        self.phone_id = None
        self.phone_obj = None
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = PeopleTable()
        pht = PhonesTable()
        pt.create()
        pht.create()
        return

    def db_insert_somethings(self):
        pt = PeopleTable()
        pht = PhonesTable()
        pt.insert_one(["Test", "Test", "Test"])
        pt.insert_one(["Test2", "Test2", "Test2"])
        pt.insert_one(["Test3", "Test3", "Test3"])
        pht.insert_one([1, "123"])
        pht.insert_one([2, "123"])
        pht.insert_one([3, "123"])

    def db_drop(self):
        pht = PhonesTable()
        pt = PeopleTable()
        pht.drop()
        pt.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр людей;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings() #заполняет после сброса и инициализации тестовыми значениями
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_people(self):
        self.person_id = -1
        menu = """Просмотр списка людей!
№\tФамилия\tИмя\tОтчество"""
        print(menu)
        lst = PeopleTable().all()
        for i in lst:
            print(i)
            # print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - просмотр телефонов человека;
    6 - ВВОДИМ НОМЕР и потом смотрим номера человека, но у него нет этого номера(?);
    7 - вводим номер телефона, потом новый номер, потом номер человека, потом этого номера нет ???
    8 - требует ввести позицию телефона, потом позицию человека и выводит всю инфу о человеке ???
    9 - выход."""
        print(menu)
        return

    def after_show_people(self, next_step):
        while True:
            if next_step == "4":
                print("Пока не реализовано!")
                return "1"
            elif next_step == "6":
                next_step = self.add_phone()
            elif next_step == "7":
                self.find_phone_by_id()
                next_step = self.edit_phone()
            elif next_step == "8":
                self.find_phone_by_id()
                next_step = self.delete_phone()
            elif next_step == "5":
                next_step = self.show_phones_by_people()
            # исправление бага с меню для телефонов при вводе неверного значения
            elif next_step != "0" and next_step != "9" and next_step != "1" and next_step != "3":
                print("Выбрано неверное значение! Повторите ввод!")
                next_step = self.read_next_step()
            else:
                return next_step

    # Форма ввода имени
    def form_first_name(self):
        while True:
            first_name = input("Введите имя (1 - отмена): ").strip()
            if first_name == "1":
                return
            if len(first_name.strip()) == 0:
                print("Имя не может быть пустым!")
            elif len(first_name.strip()) > 32:
                print("Имя имеет недопустимую длину!")
            else:
                return first_name
    # Форма ввода фамилии
    def form_last_name(self):
        while True:
            last_name = input("Введите фамилию (1 - отмена): ").strip()
            if last_name == "1":
                return
            if len(last_name.strip()) == 0:
                print("Фамилия не может быть пустой!")
            elif len(last_name.strip()) > 32:
                print("Фамилия имеет недопустимую длину!")
            else:
                return last_name
    # Форма ввода отчества
    def form_second_name(self):
        while True:
            second_name = input("Введите отчество (1 - отмена): ").strip()
            if second_name == "1":
                return
            if len(second_name.strip()) == 0:
                print("Отчество не может быть пустым!")
            elif len(second_name.strip()) > 32:
                print("Отчество имеет недопустимую длину!")
            else:
                return second_name
    # Добавление человека
    def show_add_person(self):
        data = [self.form_first_name(), self.form_last_name(), self.form_second_name()]
        # Проверяем элементы на пустоту
        for i in data:
            if i is None:
                return

        PeopleTable().insert_one(data)
        return

    # Форма ввода для телефона
    def phone_form(self):
        while True:
            phone = input("Введите номер телефона (1 - отмена): ").strip()
            if phone == "1":
                return
            elif len(phone.strip()) == 0:
                print("Телефон не может быть пустым! Введите телефон заново")
            elif len(phone.strip()) > 12:
                print("Телефон не может быть длиннее 12 символов! Введите телефон заново")
            else:
                return phone

    # Новая функция для добавление телефонов
    def add_phone(self):
        data = [self.person_id, self.phone_form()]
        PhonesTable().insert_one(data)
        return "5"

    # Вспомогательная функция, которая находит нужный номер телефона человека
    def find_phone_by_id(self):
        num = -1
        while True:
            num = input("Укажите номер строки, в которой записан интересующий Вас номер телефона (0 - отмена): ")
            if len(num.strip()) == 0:
                print("Пустая строка. Повторите ввод! ")

            if num == "0":
                return "1"

            if not num.strip().isnumeric():
                print("Неверные данные. Повторите ввод! ")

            phone = PhonesTable().find_by_position(int(num), self.person_id)

            if not phone:
                print("Введено число, неудовлетворяющее количеству телефонов!")
            else:
                self.phone_id = int(phone[0])
                self.phone_obj = phone
                break

    # Новая функция для редактирования номера телефона
    def edit_phone(self):
        phone = self.phone_form()
        PhonesTable().update(phone, self.phone_obj[1])
        return "5"

    # Новая функция для удаления номера телефона
    def delete_phone(self):
        PhonesTable().delete(self.phone_obj[1])
        return "5"

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена): ")
                while len(num.strip()) == 0:
                    num = input("Пустая строка. Повторите ввод! "
                                "Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена): ")
                if num == "0":
                    return "1"
                # проверка на то, что строка состоит из цифр
                while not num.strip().isnumeric():
                    num = input("Неверный данные. Повторите ввод! "
                                "Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена): ")
                person = PeopleTable().find_by_position(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее количеству людей!")
                else:
                    self.person_id = int(person[1])
                    self.person_obj = person
                    break
        print("Выбран человек: " + self.person_obj[2] + " " + self.person_obj[0] + " " + self.person_obj[3])
        lst = PhonesTable().all_by_person_id(self.person_id)
        # Проверяем есть ли в таблице номера телефонов для человека
        if len(lst) == 0:
            print("Нет телефонов")
        else:
            phone_show_text = """Просмотр списка телефонов!\n№\tТелефон"""
            print(phone_show_text)
            for i in range(len(lst)):
                print(str(i + 1) + "\t" + lst[i][1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    3 - ? СОЗДАНИЕ ЧЕЛОВЕКА ?
    4 - не реализовано 
    5 - ? ПРОСМОТР СПИСКА ТЕЛЕФОНОВ ?
    6 - добавление нового телефона (для выбранного человека);
    7 - редактирование номера телефона;
    8 - удаление телефона;
    9 - выход."""
        print(menu)
        return self.read_next_step()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while current_menu != "9":
            if current_menu == "0": #всегда выполняется пока не выход (9)
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_person()
                current_menu = "1"
        print("До свидания!")
        return


m = Main()
m.main_cycle()
