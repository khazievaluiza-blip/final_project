import pymysql

from local_settings import dbconfig
from mysql_connector import connect_mysql

def main_menu():
    while True:
        print("\nМеню:")
        print("1. Поиск по названию фильма")
        print("2. Поиск по жанру и диапазону годов выпуска")
        print("0. Выход")
        user_input = input("Выберите пункт меню (1, 2 или 0):")
        match user_input:
            case "1":
                title = input("Введите название или его часть: ")
                page = 1
                with pymysql.connect(**dbconfig) as connection:
                    with connection.cursor() as cursor:
                        while True:
                            print_by_title(cursor, title, page)
                            print("\nНавигация: 1 - предыдущая, 2 - следующая, 3 - выход")
                            n = input("Ваш выбор: ")
                            if n == "3":
                                break
                            elif n == "1":
                                if page > 1:
                                    page -= 1
                                else:
                                    print("Вы уже на первой странице.")
                            elif n == "2":
                                page += 1
                            else:
                                print("Неверный ввод.")
            case "2":
                with pymysql.connect(**dbconfig) as connection:
                    with connection.cursor() as cursor:
                        print_genres(cursor)
                        genre = input("Введите номер жанра: ")
                        print_year_range(cursor)
                        min_year = input("From year: ")
                        max_year = input("To year: ")
                        page = 1
                        while True:
                            print_films_by_genres_and_years(cursor, genre, min_year, max_year, page)
                            print("\nНавигация: 1 - предыдущая, 2 - следующая, 3 - выход")
                            n = input("Ваш выбор: ")
                            if n == "3":
                                break
                            elif n == "1":
                                if page > 1:
                                    page -= 1
                                else:
                                    print("Вы уже на первой странице.")
                            elif n == "2":
                                page += 1
                            else:
                                print("Неверный ввод.")
            case _:
                print("Выход из программы")
                break

def print_by_title(cursor, title, page):
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
    films = cursor.fetchall()
    print(f"\n--- Страница {page} ---")
    if not films:
        print("Нет фильмов на этой странице.")
    for t in films:
        print(t[0], f"(жанр: {t[1]})")

def print_genres(cursor):
    cursor.execute("SELECT category_id, name FROM category;")
    genres = cursor.fetchall()
    print("Available genres:")
    for t in genres:
        print(f"{t[0]}: {t[1]}")

def print_year_range(cursor):
    cursor.execute("SELECT MIN(release_year), MAX(release_year) FROM film;")
    years = cursor.fetchall()
    print("Available release years:")
    for t in years:
        print(f"Movies in the database were released between {t[0]} and {t[1]}.")

def print_films_by_genres_and_years(cursor, genre, min_year, max_year, page):
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
    films = cursor.fetchall()
    print(f"\n--- Страница {page} ---")
    if not films:
        print("Нет фильмов на этой странице.")
    for t in films:
        print(t[0], f"(жанр: {t[1]})")
main_menu()


