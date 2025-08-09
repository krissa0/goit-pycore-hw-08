#Критерії оцінювання:
# Реалізовано протокол серіалізації/десеріалізації даних за допомогою pickle
# Всі дані повинні зберігатися при виході з програми
# При новому сеансі Адресна книга повинна бути у застосунку, яка була при попередньому запуску.

##import pickle

# Приклад об'єкта для серіалізації
# data_to_serialize = {
#        'name': 'John',
#        'age': 30,
#        'city': 'New York'
# }
#
# # Серіалізація об'єкта в байти
# serialized_data = pickle.dumps(data_to_serialize)
# print("Серіалізовані дані:", serialized_data)
#
# # Запис серіалізованих даних у файл
# with open('serialized_data.pkl', 'wb') as file:
#        pickle.dump(data_to_serialize, file)
#
# # Десеріалізація з байтів
# deserialized_data = pickle.loads(serialized_data)
# print("Десеріалізовані дані:", deserialized_data)
#
# # Читання з файлу та десеріалізація
# with open('serialized_data.pkl', 'rb') as file:
# loaded_data = pickle.load(file)
# print("Дані з файлу:", loaded_data)

import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
def main():
    book = load_data()

    # Основний цикл програми

    save_data(book)  # Викликати перед виходом з програми



