import pymysql

from local_settings import dbconfig
from mysql_connector import connect_mysql

def main_menu():
    while True:
        print("\nМеню:")
        print("1. Поиск по названию фильма")
        print("2. Поиск информации о клиентах")
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
                print("<UNK> <UNK> <UNK> <UNK> 2")
            case _:
                print("Выход из программы")
                break

def print_by_title(cursor, title, page=1):
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

main_menu()


