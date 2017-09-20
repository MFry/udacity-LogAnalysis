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


def set_article_popularity(cur):
    cur.execute('''
                CREATE TEMPORARY TABLE article_hits AS (
                  SELECT
                    title,
                    total,
                    articles.author AS author_id
                  FROM url_hits
                  LEFT JOIN articles
                  ON POSITION(articles.slug IN url_hits.path) > 0
                )
                ''')


def set_authors_popularity(cur):
    cur.execute('''
                CREATE TEMPORARY TABLE authors_popularity AS (
                  SELECT
                    name,
                    total
                  FROM article_hits
                  LEFT JOIN authors
                  ON author_id = authors.id
                )
                ''')


def getMostPopularArticles(cur, top=3):
    cur.execute('''
                 SELECT *
                 FROM article_hits
                 LIMIT %s;
                ''', (top, ))
    return cur.fetchall()


def listAllAuthorsPopularity(cur, top=3):
    cur.execute('''
                SELECT 
                   *
                FROM authors_popularity
                LIMIT %s
                ''', (top,))
    return cur.fetchall()


if __name__ == '__main__':
    with get_cursor() as cur:
        cur.execute('SELECT * FROM log LIMIT 10;')
        data = cur.fetchall()
        pprint(data)
        set_url_popularity(cur)
        set_article_popularity(cur)
        set_authors_popularity(cur)
        pprint(getMostPopularArticles(cur))
        pprint(listAllAuthorsPopularity(cur))
