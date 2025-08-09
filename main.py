from serialization import save_data, load_data # Серіалізація, десеріалізація
from task1 import AddressBook, Record, add_contact, change_phone, show_phone, show_all, add_birthday, show_birthday, birthdays, greet, exit_program, parse_input


def main():
    book = load_data() #Книга
    print('Это бот-помощник.')

    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ['exit', 'close']:
            save_data(book)
            print('До побачення')
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
                print('До побачення')
                break
            print(result)
        else:
            print(f'Команда "{command}" не знайдена.')

if __name__ == '__main__':
    main()

