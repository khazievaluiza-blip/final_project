from mysql_connector import search_by_title, print_genres, print_year_range, search_by_genre_and_years
from log_writer import write_log
from log_stats import pop_requests, latest_requests
from formatter import print_menu
from colorama import Fore

def main_menu()-> None:
    """
    The function launches a user menu for searching movies in database.
    When a menu option is selected, the corresponding search function is executed.
    """
    while True:
        print_menu()
        match input("Enter your choice: "):
            case "1":
                title = input("Enter a keyword or part of the movie title: ")
                write_log('search_by_title', title)
                search_by_title(title)
            case "2":
                valid_genres = print_genres()
                genre = input("Enter genre number: ")
                while genre not in valid_genres:
                    genre = input("Invalid genre. Please try again: ")
                years = print_year_range()
                min_year_choice = int(input("From year: "))
                while min_year_choice < years[0][0] or min_year_choice > years[0][1]:
                    min_year_choice = int(input("Invalid year. Please try again: "))
                max_year_choice = input("To choose a single year, just press Enter. To define a range, enter the second year: ")
                if max_year_choice == "":
                    max_year_choice = min_year_choice
                else:
                    max_year_choice = int(max_year_choice)
                while max_year_choice < years[0][0] or max_year_choice > years[0][1]:
                    max_year_choice = input("Invalid year. Please try again: ")
                write_log('search_by_genre_and_years', genre, min_year_choice, max_year_choice)
                search_by_genre_and_years(genre, min_year_choice, max_year_choice)
            case "3":
                print(f"{Fore.MAGENTA}{"\nMost frequent search queries:"}")
                pop_requests()
            case "4":
                print(f"{Fore.MAGENTA}{"\n5 last search queries:"}")
                latest_requests()
            case "0":
                print("Exit program")
                break
            case _:
                print("Invalid input. Please try again.")

if __name__ == "__main__":
    main_menu()


