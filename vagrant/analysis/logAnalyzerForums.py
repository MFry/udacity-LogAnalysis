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


def set_url_popularity(cur):
    cur.execute('''
                CREATE TEMPORARY TABLE url_hits AS (
                  SELECT 
                     path,
                     COUNT (path) AS total
                    FROM
                     log
                    WHERE
                     path is DISTINCT FROM '/'
                    GROUP BY
                     path
                    ORDER BY total DESC
                )
                ''')


def getMostPopularArticles(cur, top=3):
        cur.execute('''
                     SELECT *
                     FROM url_hits
                     LIMIT %s;
                    ''', (top, ))
        return cur.fetchall()


def listAllAuthorsPopularity():
    with get_cursor() as cur:
        cur.execute('''
                    SELECT 
                       *
                    FROM
                      url_hits
                     INNER JOIN articles ON 
                    ''')


if __name__ == '__main__':
    with get_cursor() as cur:
        cur.execute('SELECT * FROM log LIMIT 10;')
        data = cur.fetchall()
        pprint(data)
        set_url_popularity(cur)
        pprint(getMostPopularArticles(cur))
