# flake8: noqa

# This is a workaround for sqlalchemy 2.0 returning Sequence instead of list, when
#   calling .all() on a result.
# https://github.com/sqlalchemy/sqlalchemy/discussions/9138

from typing import Any, Optional, Tuple, overload

from sqlalchemy import Executable, Result, Row, ScalarResult
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
from sqlalchemy.engine.result import _R, _T, _TP
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import TypedReturnsRows


class ScalarResultWrapper(ScalarResult[_R]):
    def all(self) -> list[_R]:
        """Return all scalar values in a list.

        Equivalent to :meth:`_engine.Result.all` except that
        scalar values, rather than :class:`_engine.Row` objects,
        are returned.

        """
        return self._allrows()


class ResultWrapper(Result[_TP]):
    """So cool."""

    def scalars(self: Result[Tuple[_T]]) -> ScalarResultWrapper[_T]:  # type: ignore
        return super().scalars()  # type: ignore

    def all(self) -> list[Row[_TP]]:
        return self._allrows()


class AsyncSessionWrapper(AsyncSession):
    """wow"""

    @overload  # type: ignore
    async def execute(
        self,
        statement: TypedReturnsRows[_T],
        params: Optional[_CoreAnyExecuteParams] = None,
    ) -> ResultWrapper[_T]:
        ...

    @overload
    async def execute(
        self,
        statement: Executable,
        params: Optional[_CoreAnyExecuteParams] = None,
    ) -> ResultWrapper[Any]:
        ...

    async def execute(
        self,
        statement: Executable,
        params: Optional[_CoreAnyExecuteParams] = None,
    ) -> ResultWrapper[Any]:
        return await super().execute(statement, params)  # type: ignore
