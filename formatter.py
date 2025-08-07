from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

init(autoreset=True)

def print_menu() -> None:
    """Displays the main user interface menu using the colorama library."""
    print(f"{Fore.MAGENTA}{"\n--- Find movies in Sakila ---"}")
    print(f"{Fore.CYAN}{"\nChoose an option:"}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Search by movie title")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Search by genre and release year")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} View most frequent search queries:")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} View recent search queries")
    print(f"{Fore.CYAN}0.{Style.RESET_ALL} Exit")

def print_film_info(title: str, year: int, genre: str, language: str, length: str, rating: str, description: str, actors: str) -> None:
    """Displays detailed information about a film"""
    console = Console()
    info = Text()
    info.append(f"Title: {title}\n")
    info.append(f"Year: {year}   Genre: {genre}   Language: {language}\n")
    info.append(f"Length: {length} min   Rating: {rating}\n")
    info.append(f"Description: {description}\n")
    info.append(f"Actors: {actors}")

    panel = Panel(info, box=box.ROUNDED, padding=(1, 2), expand=False, border_style="green")
    console.print(panel)
