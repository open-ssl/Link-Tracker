from fastapi import APIRouter
from typing import Dict, Optional

from http import HTTPStatus
from utils.db_helpers import insert_new_links_for_user, get_links_for_interval
from utils.helpers import Const, ConstConfig, LinkParser
from utils.router import Router
from utils.schemas import LinksRequestModel

event_router = APIRouter(tags=[ConstConfig.ROUTER_EVENT_TAG])


def get_500_response() -> Dict:
    """
    Возвращает обьект для Response со статусом 500
    :return: Dict
    """
    return {Const.STATUS: HTTPStatus.INTERNAL_SERVER_ERROR}


def get_400_response() -> Dict:
    """
    Возвращает обьект для Response со статусом 400
    :return: Dict
    """
    return {Const.STATUS: HTTPStatus.BAD_REQUEST}


def get_404_response() -> Dict:
    """
    Возвращает обьект для Response со статусом 404
    :return: Dict
    """
    return {Const.STATUS: HTTPStatus.NOT_FOUND}


def get_200_response() -> Dict:
    """
    Возвращает обьект для Response со статусом 200
    :return: Dict
    """
    return {Const.DATA: HTTPStatus.OK}


@event_router.post(Router.VISITED_LINKS)
def post_visited_links(request: LinksRequestModel):
    """
    POST запрос на запись посещенных пользователем ссылок
    :param request: list[str] - url-ы посещенных сайтов
    :return: http.Response
    """
    if not request.links:
        return get_404_response()

    links = LinkParser.get_unique_domains_from_raw_urls(request.links)
    if not links:
        return get_400_response()

    if insert_new_links_for_user(links):
        return get_200_response()

    return get_500_response()


@event_router.get(Router.VISITED_DOMAINS, response_model=Dict)
def get_visited_domains(from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None):
    """
    GET запрос на вычитку посещенных доменов
    :param from_timestamp: начало интервала
    :param to_timestamp: конец интервала
    :return: http.Response
    """

    if (not from_timestamp and not to_timestamp) or (from_timestamp and to_timestamp and from_timestamp > to_timestamp):
        return get_400_response()

    domains = get_links_for_interval(from_timestamp, to_timestamp)
    if domains is None:
        return get_500_response()

    return {Const.DOMAINS: LinkParser.get_unique_domains_from_list_urls(domains), Const.STATUS: HTTPStatus.OK}
