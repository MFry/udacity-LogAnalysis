import psycopg2
from contextlib import contextmanager
from pprint import pprint


def connect():
    """

    :return:
    """
    return psycopg2.connect("dbname=forum")


@contextmanager
def get_cursor():
    conn = connect()
    cursor = conn.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def getMostPopularArticles(top=3):
    with get_cursor() as cur:
        cur.execute('''
                     SELECT 
                       path,
                       COUNT (path) AS total
                     FROM
                       log
                     GROUP BY
                       path
                     ORDER BY total DESC
                     LIMIT %s;
                    ''', (top, ))
        return cur.fetchall()


if __name__ == '__main__':
    with get_cursor() as cur:
        cur.execute('SELECT * FROM log LIMIT 10;')
        data = cur.fetchall()
        pprint(data)
        pprint(getMostPopularArticles())
