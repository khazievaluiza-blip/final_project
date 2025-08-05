from mysql_connector import search_by_title, print_genres, print_year_range, search_by_genre_and_years
from log_writer import write_log, pop_requests, latest_requests
from formatter import print_menu

def main_menu()-> None:
    """The function launches a user menu for searching movies in database.
        When a menu option is selected, the corresponding search function is executed.
    """
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                title = input("Enter a keyword or part of the movie title: ")
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


