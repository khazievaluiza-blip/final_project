from mysql_connector import search_by_title, print_genres, print_year_range, search_by_genre_and_years
from log_writer import write_log, pop_requests, latest_requests

def main_menu():
    while True:
        print("\nМеню:")
        print("1. Поиск по названию фильма")
        print("2. Поиск по жанру и диапазону годов выпуска")
        print("3. Популярные запросы")
        print("4. Последние запросы")
        print("0. Выход")
        choice = input("Выберите пункт меню: ")

        match choice:
            case "1":
                title = input("Введите название или его часть: ")
                write_log('search_by_title', title)
                search_by_title(title)
            case "2":
                print_genres()
                genre = input("Введите номер жанра: ")
                print_year_range()
                min_year = input("From year: ")
                max_year = input("To year: ")
                write_log('search_by_genre_and_years', genre, min_year, max_year)
                search_by_genre_and_years(genre, min_year, max_year)
            case "3":
                print("Самые популярные запросы:")
                pop_requests()
            case "4":
                print("5 последних запросов")
                latest_requests()
            case "0":
                print("Выход из программы.")
                break
            case _:
                print("Неверный выбор.")



main_menu()


