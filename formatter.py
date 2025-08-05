from colorama import init, Fore, Back, Style

init(autoreset=True)

def print_menu() -> None:
    """Displays the main user interface menu."""
    print(f"{Fore.MAGENTA}{"\n--- Find movies in Sakila ---"}")
    print(f"{Fore.CYAN}{"\nChoose an option:"}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Search by movie title")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Search by genre and release year")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} View most popular search queries")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} View recent search queries")
    print(f"{Fore.CYAN}0.{Style.RESET_ALL} Exit")

def print_film_info(title, year, genre, language, length, rating, description, actors):
    print(f"{Style.BRIGHT}{Fore.CYAN}Title: {title}")
    print(f"Year: {year}   Genre: {genre}   Language: {language}")
    print(f"Length: {length} min   Rating: {rating}")
    print(f"Description: {description}")
    print(f"Actors: {actors}")
    print(f"{Fore.MAGENTA}{'-' * 60}")