from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, gt=0, description="Порядковый номер страницы")]
    per_page: Annotated[int | None, Query(None, gt=0, lt=100, description="Кол-во элементов на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]
