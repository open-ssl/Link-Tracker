from http import HTTPStatus
from fastapi import HTTPException
from pydantic import BaseModel


class LinksRequestModel(BaseModel):
    """
    Модель посещенных ссылок
    """
    links: list[str]

    @classmethod
    def validate_links(cls) -> list:
        """
        Валидация входящих ссылок
        :param links: (list) - список ссылок
        :return:
        """
        if len(cls.links) == 0:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Empty links list",
            )

        return cls.links
