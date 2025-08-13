from serialization import save_data, load_data # Серіалізація, десеріалізація
from task1 import AddressBook, Record, add_contact, change_phone, show_phone, show_all, add_birthday, show_birthday, birthdays, greet, exit_program, parse_input
from consple_ui import Console2 # Імпортуємо класс з файлу (Абстрактний класс для виведення інформації користувачу)

def main():
    book = load_data() #Книга
    console = Console2()
    console.show_message("Це бот-помічник!")
    console.show_message("""Доступні команди:
'hello': greet,
'add': add_contact,
'change': change_phone,
'phone': show_phone,
'all': show_all,
'add-birthday': add_birthday,
'show-birthday': show_birthday,
'birthdays': birthdays
""")

    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ['exit', 'close']:
            save_data(book)
            console.show_message('До побачення')
            break

        commands = {
            'hello': greet,
            'add': add_contact,
            'change': change_phone,
            'phone': show_phone,
            'all': show_all,
            'add-birthday': add_birthday,
            'show-birthday': show_birthday,
            'birthdays': birthdays,
        }

        handler = commands.get(command)
        if handler:
            result = handler(args, book)
            if result == 'exit':
                save_data(book)
                console.show_message('До побачення!')
                break
            console.show_result(result)
        else:
            console.show_message(f'Команда "{command}" не знайдена.')

if __name__ == '__main__':
    main()

