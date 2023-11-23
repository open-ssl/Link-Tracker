from typing import Optional
from utils import sql_templates
from utils.db import fetch_data_from_db, insert_data_in_db
from utils.log_helpers import log_error_in_file


def generate_sql_template_array_value(array: list) -> str:
    """
    Возвращает корректное значение массива для вставки в SQL-шаблон
    :return: str - значение для вставки в шаблон
    """
    text_arr_value = ', '.join([f'{item}' for item in array])
    return "'{" + f'{text_arr_value}' + "}'"


def insert_new_links_for_user(links: list[str]):
    """
    Вставка новых ссылок для пользователя
    :param: links (list[str]): массив ссылок для вставки
    :return: bool - статус операции
    """
    try:
        insert_data_in_db(
            sql_templates.INSERT_NEW_LINKS_TEMPLATE,
            generate_sql_template_array_value(links)
        )
    except Exception as _:
        # Различные виды ошибок не описаны специально
        log_error_in_file()
        return None

    return True


def create_visited_domains_template(from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None):
    """
    Создание шаблона для запроса ссылок в интервале
    :param from_timestamp: начало интервала
    :param to_timestamp: конец интервала
    :return: шаблон для запроса в БД
    """
    base_template = sql_templates.SELECT_VISITED_DOMAINS_IN_INTERVAL_TEMPLATE
    if not from_timestamp and not to_timestamp:
        return None
    if from_timestamp and to_timestamp:
        return base_template + f"between to_timestamp({from_timestamp}) and to_timestamp({to_timestamp})"
    elif from_timestamp:
        return base_template + f">= to_timestamp({from_timestamp})"

    return base_template + f"<= to_timestamp({to_timestamp})"


def get_links_for_interval(from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None):
    """
    Выгрузка ссылок в интервале
    :param from_timestamp: начало интервала
    :param to_timestamp: конец интервала
    :return: bool - статус операции
    """
    data = None
    try:
        sql_template = create_visited_domains_template(from_timestamp, to_timestamp)
        if not sql_template:
            return data
        data = fetch_data_from_db(sql_template)
    except Exception as _:
        # Различные виды ошибок не описаны специально
        log_error_in_file()
        return data

    return data or list()
