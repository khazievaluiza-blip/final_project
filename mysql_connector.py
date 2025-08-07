import pymysql
from dotenv import load_dotenv
import os
from typing import Callable
from formatter import print_film_info
from colorama import Fore, Style

load_dotenv()

dbconfig = {
    'host': os.getenv("HOST"),
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'database': os.getenv("DATABASE"),
}

def connect_mysql(func: Callable) -> Callable:
    """
    Decorator for connecting to MongoDB by using context managers `with`
    and handling errors. This decorator passes the database cursor as the first argument
    to the wrapped function.
    """
    def wrapper(*args):
        try:
            with pymysql.connect(**dbconfig) as connection:
                with connection.cursor() as cursor:
                    return func(cursor, *args)
        except pymysql.MySQLError as e:
            print(f"Connection error: {e}")
            return None
    return wrapper

def pagination(func: Callable) -> Callable:
    """
    Decorator that adds paginated output for displaying information about films
    using `print_film_info`. It allows the user to navigate through pages or exit
    the pagination.
    """
    def wrapper(*args):
        page = 1
        while True:
            films = func(*args, page=page)
            print(f"\n{Fore.MAGENTA}{'-' * 56} Page {page} {'-' * 56}")
            if not films:
                print("No movies on this page")
            for t in films:
                print_film_info(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7])
            print(f"{Fore.CYAN}\nChoose an option: 1{Style.RESET_ALL} - Next Page, {Fore.CYAN}any other{Style.RESET_ALL} - Exit to main menu")
            nav = input("Enter your choice: ")
            if nav == "1":
                page += 1
            else:
                break
    return wrapper

@connect_mysql
def print_genres(cursor) -> list[str]:
    """
    The function retrieves a list of all genre IDs and names from the database,
    prints them to the console with formatting using the Colorama library,
    and returns a list of valid genre IDs as strings.

    :param cursor: A database cursor object provided by the `connect_mysql` decorator,
    which is used to execute the SQL query.
    :return: A list of valid genre IDs (as strings) for input validation.
    """
    cursor.execute("SELECT category_id, name FROM category;")
    genres = cursor.fetchall()
    valid_genres = []
    print(f"{Fore.CYAN}{"\nAvailable genres:"}")
    for t in genres:
        valid_genres.append(str(t[0]))
        print(f"{Fore.CYAN}{t[0]}. {Style.RESET_ALL}{t[1]}")
    return valid_genres

@connect_mysql
def print_year_range(cursor):
    """
    The function retrieves the minimum and maximum release years from the database,
    prints them to the console with formatting using the Colorama library,
    and returns a range of valid years.

    :param cursor: A database cursor object provided by the `connect_mysql` decorator,
    which is used to execute the SQL query.
    :return: A range object containing all valid years from the earliest to the latest film release.
    """
    cursor.execute("SELECT MIN(release_year), MAX(release_year) FROM film;")
    years = cursor.fetchall()

    print(f"""Movies in the database were released between {Fore.CYAN}{years[0][0]}{Style.RESET_ALL} and {Fore.CYAN}{years[0][1]}.
            You can select a single year or a range of years.""")
    return years

@connect_mysql
@pagination
def search_by_title(cursor, title: str, page: int) ->list[tuple]:
    """
    The function receives a keyword, a database cursor and a page number from the decorators,
    and performs a search for films whose titles contain
    the given keyword (full or partial match).
    The results are returned paginated (10 records per page)
    and include detailed film information such as
    release year, genre, language, duration, rating, description, and actors.

    :param cursor: A database cursor object provided by the `connect_mysql` decorator,
    which is used to execute the SQL query.
    :param title: A keyword or substring to search for in film titles
    :param page: The page number for pagination provided by the `pagination` decorator.
    :return: A list of tuples, where each tuple contains:
            title, release_year, genre, language, length, rating, description, actors
    """
    offset = (page - 1) * 10
    title_mask = f"%{title}%"
    cursor.execute("""
                    SELECT f.title, f.release_year, c.name, l.name, f.length, 
                       CASE f.rating
                            WHEN 'G' THEN 'G: General Audiences'
                            WHEN 'PG' THEN 'PG: Parental Guidance Suggested'
                            WHEN 'PG-13' THEN 'PG-13: Some material may be inappropriate for children under 13'
                            WHEN 'R' THEN 'R: Under 17 requires accompanying parent or adult guardian'
                            WHEN 'NC-17' THEN 'NC-17: Only for adults (18+)'
                            ELSE 'Other'
                        END AS rating_text, 
                        f.description, group_concat(concat(a.first_name, " ", a.last_name) SEPARATOR ', ') AS actors
                    FROM film as f
                        LEFT JOIN film_category as fc USING (film_id)
                        LEFT JOIN category as c USING (category_id)
                        LEFT JOIN language as l USING (language_id)
                        LEFT JOIN film_actor as fa USING (film_id)
                        LEFT JOIN actor as a USING (actor_id)
                    WHERE f.title LIKE %s
                    GROUP BY f.title
                    LIMIT 10 OFFSET %s
                   """, (title_mask, offset))
    return cursor.fetchall()

@connect_mysql
@pagination
def search_by_genre_and_years(cursor, genre: str, min_year: str, max_year: str, page: int) ->list[tuple]:
    """
    The function receives a cursor and page number from the decorator, a genre, a minimum and maximum year
    and searches the database for movies of the corresponding genre in a range of release years.
    The results are returned paginated (10 records per page)
    and include detailed film information such as
    release year, genre, language, duration, rating, description, and actors.

    :param cursor: A database cursor object provided by the `connect_mysql` decorator,
    which is used to execute the SQL query.
    :param genre: A film genre name to search for.
    :param min_year: The minimum year to search for.
    :param max_year: The maximum year to search for.
    :param page: The page number for pagination provided by the `pagination` decorator.
    :return: A list of tuples, where each tuple contains:
    title, release_year, genre, language, length, rating, description, actors
    """
    offset = (page - 1) * 10
    cursor.execute("""
                    SELECT f.title, f.release_year, c.name, l.name, f.length, 
                       CASE f.rating
                            WHEN 'G' THEN 'G: General Audiences'
                            WHEN 'PG' THEN 'PG: Parental Guidance Suggested'
                            WHEN 'PG-13' THEN 'PG-13: Some material may be inappropriate for children under 13'
                            WHEN 'R' THEN 'R: Under 17 requires accompanying parent or adult guardian'
                            WHEN 'NC-17' THEN 'NC-17: Only for adults (18+)'
                            ELSE 'Other'
                        END AS rating_text, 
                       f.description, group_concat(concat(a.first_name, " ", a.last_name) SEPARATOR ', ') AS actors
                    FROM film as f
                        LEFT JOIN film_category as fc USING (film_id)
                        LEFT JOIN category as c USING (category_id)
                        LEFT JOIN language as l USING (language_id)
                        LEFT JOIN film_actor as fa USING (film_id)
                        LEFT JOIN actor as a USING (actor_id)
                    WHERE c.category_id = %s
                    AND f.release_year BETWEEN %s AND %s
                    GROUP BY f.title
                    LIMIT 10 OFFSET %s
                   """, (genre, min_year, max_year, offset))
    return cursor.fetchall()

if __name__ == '__main__':
    print(search_by_title("love"))