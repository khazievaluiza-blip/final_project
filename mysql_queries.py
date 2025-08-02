def do_query(query_type, parameters_dict):
    connection = connect_mysql()

    if not connection:
        return

    try:
        with connection:
            with connection.cursor() as cursor:

                if query_type == 'search_by_keyword':
                    cursor.execute(query_search_by_keyword,
                                   queries_dict[query_type])


                elif query_type == 'get_all_genres':
                    cursor.execute("SELECT name FROM category")
                    return [row['name'] for row in cursor.fetchall()]

                elif query_type == 'get_min_max_years':
                    get_min_max_years(cursor)

                elif query_type == 'search_by_genre_and_years':
                    search_by_genre_and_years(cursor, genre, year_from, year_to, offset=0, limit=10)

    except pymysql.MySQLError as e:
        print(f"MySQL error in {query_type}: {e}")
        return []

