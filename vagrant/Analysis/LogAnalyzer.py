import psycopg2
from contextlib import contextmanager


def connect():
    """

    :return:
    """
    return psycopg2.connect("dbname=news")


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


if __name__ == '__main__':
    with get_cursor() as cur:
        data = cur.execute('SELECT * FROM log LIMIT 10')
        print(data)
