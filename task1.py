from collections import UserDict
from datetime import datetime, timedelta

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: недостатньо аргументів для команди."
        except (KeyError, AttributeError):
            return "Error: контакт не знайдено."
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Номер повинен містити 10 цифр')
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Невірний формат дати")
        self.value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number: str):
        phone = Phone(number)
        self.phones.append(phone)

    def remove_phone(self, number: str):
        for p in self.phones:
            if p.value == number:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_number: str, new_number: str):
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                return True
        return False

    def find_phone(self, number: str):
        for p in self.phones:
            if p.value == number:
                return p
        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().date()
        bday_date = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()
        next_birthday = bday_date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones_str = ', '.join(p.value for p in self.phones) if self.phones else "Немає"
        bday_str = self.birthday.value if self.birthday else "Немає"
        return f"{self.name.value}: Телефони [{phones_str}], день народження: {bday_str}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                days = record.days_to_birthday()
                if days is not None and 0 <= days <= 7:
                    birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                    next_birthday = birthday_date.replace(year=today.year)
                    if next_birthday < today:
                        next_birthday = next_birthday.replace(year=today.year + 1)
                    weekday = next_birthday.weekday()
                    if weekday == 5:
                        next_birthday += timedelta(days=2)
                    elif weekday == 6:
                        next_birthday += timedelta(days=1)

                    upcoming.append({
                        "name": record.name.value,
                        "birthday": next_birthday.strftime("%d.%m.%Y")
                    })
        return upcoming

    def __str__(self):
        if not self.data:
            return "Адресна книга порожня"
        return '\n'.join(str(record) for record in self.data.values())

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record.edit_phone(old_phone, new_phone):
        return "Телефон оновлено."
    else:
        return "Старий номер не знайдено."

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    phones = ', '.join(p.value for p in record.phones) if record.phones else "немає телефонів"
    return f"{name}: {phones}"

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    return f"День народження додано для {name}"

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record.birthday:
        return f"День народження {name}: {record.birthday.value}"
    else:
        return f"Для контакту {name} не встановлено день народження."

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Немає днів народжень у найближчі 7 днів."
    lines = []
    for item in upcoming:
        lines.append(f"{item['name']} Привітати {item['birthday']}")
    return "\n".join(lines)

def show_all(args, book: AddressBook):
    return str(book)

def greet(args, book: AddressBook):
    return "Як я можу допомогти?"

def exit_program(args, book: AddressBook):
    return "exit"

def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args

def main():
    book = AddressBook()
    print("Вітаю, це бот-помічник!")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення")
            break

        commands = {
            "hello": greet,
            "add": add_contact,
            "change": change_phone,
            "phone": show_phone,
            "all": show_all,
            "add-birthday": add_birthday,
            "show-birthday": show_birthday,
            "birthdays": birthdays,
        }

        handler = commands.get(command)
        if handler:
            result = handler(args, book)
            if result == "exit":
                print("До побачення")
                break
            print(result)
        else:
            print("Команду не знайдено")

if __name__ == "__main__":
    main()
