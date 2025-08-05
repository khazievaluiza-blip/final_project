import pymysql
from dotenv import load_dotenv
import os
from formatter import print_film_info
from colorama import init, Fore, Back, Style

load_dotenv()

dbconfig = {
    'host': os.getenv("HOST"),
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'database': os.getenv("DATABASE"),
}

def connect_mysql(func):
    """
    Decorator function for connecting to MongoDB by using context managers `with`
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

def pagination(func):
    """Добавляет пагинацию с выводом фильмов."""
    def wrapper(*args):
        page = 1
        print(f"\n{Fore.MAGENTA}{'-'*56} Page {page} {'-' * 56}")
        while True:
            films = func(*args, page=page)
            if not films:
                print("Нет фильмов на этой странице.")
            for t in films:
                print_film_info(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7])
            print(f"{Fore.CYAN}\nChoose an option: 1{Style.RESET_ALL} - Next Page, {Fore.CYAN}0{Style.RESET_ALL} - Exit")
            nav = input("Enter your choice: ")
            match nav:
                case "0":
                    break
                case "1":
                    page += 1
                case _:
                    print("Invalid input. Please try again.")
                    continue
    return wrapper

@connect_mysql
def print_genres(cursor):
    cursor.execute("SELECT category_id, name FROM category;")
    genres = cursor.fetchall()
    valid_genres = []
    print("Available genres:")
    for t in genres:
        valid_genres.append(t[0])
        print(f"{t[0]}: {t[1]}")
    return valid_genres

@connect_mysql
def print_year_range(cursor):
    cursor.execute("SELECT MIN(release_year), MAX(release_year) FROM film;")
    years = cursor.fetchall()
    valid_years = range(years[0][0], years[0][1] + 1)
    print("Available release years:")
    for t in years:
        print(f"Movies in the database were released between {t[0]} and {t[1]}.")
    return valid_years

@connect_mysql
@pagination
def search_by_title(cursor, title, page):
    offset = (page - 1) * 10
    title_mask = f"%{title}%"
    cursor.execute("""
                   SELECT f.title, f.release_year, c.name, l.name, f.length, f.rating, f.description, group_concat(concat(a.first_name, " ", a.last_name) SEPARATOR ', ') AS actors
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
def search_by_genre_and_years(cursor, genre, min_year, max_year, page):
    offset = (page - 1) * 10
    cursor.execute("""
                   SELECT f.title, f.release_year, c.name, l.name, f.length, f.rating, f.description, group_concat(concat(a.first_name, " ", a.last_name) SEPARATOR ', ') AS actors
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
