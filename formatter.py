from colorama import init, Fore, Back, Style

init(autoreset=True)

def print_film_info(title, year, genre, language, length, rating, description, actors):
    print(f"{Style.BRIGHT}{Fore.CYAN}Title: {title}")
    print(f"Year: {year}   Genre: {genre}   Language: {language}")
    print(f"Length: {length} min   Rating: {rating}")
    print(f"Description: {description}")
    print(f"Actors: {actors}")
    print(f"{Fore.MAGENTA}{'-' * 60}")