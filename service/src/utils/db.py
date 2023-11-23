from config.data import DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT
from utils.log_helpers import log_error_in_file
from threading import Lock
from psycopg2 import connect as create_db_connect


def get_db_connection():
    """
    :return: Экземпляр соединения с базой данных
    """
    conn = None
    try:
        conn = create_db_connect(dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT)
        conn.autocommit = True
    except Exception as _:
        print("Unable to connect the database")
        log_error_in_file()

    return conn


def fetch_data_from_db(query_template, *args, fetchone=True, fetchall_as_one=True):
    """
    Запрос в базу данных на извлечение записей из выборки
    :param query_template: шаблон для запроса в БД
    :param fetchone: bool - выгружать только первую из выборки или все
    :param fetchall_as_one: bool - получать все результаты из итоговой выборки как одно поле
    :param args: аргументы для вставки в шаблон запроса
    :return: Результаты запроса
    """
    connection = get_db_connection()
    if not connection:
        return

    with Lock():
        with connection as conn:
            cursor = conn.cursor()

            query_template = query_template.format(*args)
            cursor.execute(query_template)
            if fetchone:
                return cursor.fetchone()[0]
            if fetchall_as_one:
                return cursor.fetchall()[0]
            return cursor.fetchall()


def insert_data_in_db(query_template, *args):
    """
    Запрос в базу данных на вставку или изменение записей
    :param query_template: шаблон для запроса в БД
    :param args: аргументы для вставки в шаблон запроса
    :return: None
    """
    connection = get_db_connection()
    if not connection:
        return

    with Lock():
        with connection as conn:
            cursor = conn.cursor()
            query_template = query_template.format(*args)
            cursor.execute(query_template)
