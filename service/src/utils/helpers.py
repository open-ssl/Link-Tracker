from datetime import date, datetime
from re import match as re_match
from urllib.parse import urlsplit


class Const:
    """
    Обьект текстовых констант
    """
    DATA = "data"
    DOMAINS = "domains"
    STATUS = "status"
    LINKS = "links"


class ConstConfig:
    """
    Обьект конфига для запуска приложения
    """
    PROJECT_TITLE = "Link tracker"
    ROUTER_EVENT_TAG = "event"


class LinkParser:
    _SHORT_URL_RE_PATTERN = r"((?:[\w-]+)(?:\.[\w-]+)+)"

    @classmethod
    def get_unique_domains_from_raw_urls(cls, urls: list[str]) -> list:
        """
        Получение уникальных доменных имен из входных url
        :param urls: list[str] - посещенные пользователем ссылки
        :return: list - уникальные посещенные домены
        """
        domains = list()
        for url in urls:
            parsed_url = urlsplit(url)
            if parsed_url.netloc:
                domains.append(parsed_url.netloc)
                continue

            if re_match(cls._SHORT_URL_RE_PATTERN, url):
                domains.append(url)

        return list(set(domains))

    @classmethod
    def get_unique_domains_from_list_urls(cls, urls: list[list]) -> list:
        """
        Получение уникальных доменных имен из вложенных данных по url
        :param urls: list[list] - список всех посещенных доменов некоторыз пользователем
        :return: list - уникальные посещенные домены
        """
        domains = set()
        for url_data in urls:
            domains.update(url_data)

        return list(domains)


def get_current_data_and_time() -> tuple:
    """
    Получение серверной даты в времени
    :return: tuple - дата и время
    """
    data_for_file = date.today().strftime("%m-%d-%Y")
    time_for_file = datetime.now().strftime("%H:%M:%S")
    return data_for_file, time_for_file
