#! /vagrant/analysis/py36env/bin/python3.6
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


def set_requests_by_day(cur):
    cur.execute('''
                CREATE TEMPORARY TABLE total_requests_per_day AS (
                  SELECT
                    log.time::DATE as time,
                    COUNT(log.time::DATE) AS hits -- Loses timezone information
                  FROM log
                  GROUP BY log.time::DATE
                )
                ''')


def get_most_popular_articles(cur, top=3):
    cur.execute('''
                 SELECT *
                 FROM article_hits
                 LIMIT %s;
                ''', (top, ))
    return cur.fetchall()


def get_most_popular_authors(cur, top=3):
    cur.execute('''
                SELECT 
                   *
                FROM authors_popularity
                LIMIT %s
                ''', (top,))
    return cur.fetchall()


def get_largest_error_frequency_by_day(cur, top=1):
    cur.execute('''
                WITH total_errors_per_day AS (
                  SELECT
                    log.time::DATE as time,
                    COUNT(log.time::DATE) AS hits -- Loses timezone information
                  FROM log
                  WHERE log.status ~ '4[0-9]{2}' 
                  GROUP BY log.time::DATE
                )
                SELECT 
                 total_errors_per_day.time as time,
                 total_errors_per_day.hits/total_requests_per_day.hits::FLOAT as percentage_errors
                FROM total_errors_per_day
                LEFT JOIN total_requests_per_day
                ON total_requests_per_day.time = total_errors_per_day.time
                WHERE total_errors_per_day.hits/total_requests_per_day.hits::FLOAT > 0.01
                ''')
    return cur.fetchall()


if __name__ == '__main__':
    with get_cursor() as cur:
        print('Testing database access. Getting first ten rows from table log.')
        cur.execute('SELECT * FROM log LIMIT 10;')
        data = cur.fetchall()
        pprint(data)
        set_url_popularity(cur)
        set_article_popularity(cur)
        set_authors_popularity(cur)
        set_requests_by_day(cur)
        print('Most popular articles:')
        pprint(get_most_popular_articles(cur))
        print('Most popular authors:')
        pprint(get_most_popular_authors(cur))
        print('Largest day with errors:')
        pprint(get_largest_error_frequency_by_day(cur))
