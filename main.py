import mysql_connector



def main_menu():
    while True:
        print("\nМеню:")
        print("1. Поиск по названию фильма")
        print("2. Поиск по жанру и диапазону годов выпуска")
        print("0. Выход")
        choice = input("Выберите пункт меню: ")

        match choice:
            case "1":
                title = input("Введите название или его часть: ")
                mysql_connector.search_by_title(title)
            case "2":
                mysql_connector.print_genres()
                genre = input("Введите номер жанра: ")
                mysql_connector.print_year_range()
                min_year = input("From year: ")
                max_year = input("To year: ")
                mysql_connector.search_by_genre_and_years(genre, min_year, max_year)
            case "0":
                print("Выход из программы.")
                break
            case _:
                print("Неверный выбор.")



main_menu()


