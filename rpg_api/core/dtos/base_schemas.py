from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar("DataT", bound=BaseModel | list[BaseModel])
ValueT = TypeVar("ValueT", bound=Any)


class GenericModel(BaseModel, Generic[DataT]):
    model: DataT


class DataResponse(BaseModel, Generic[DataT]):
    """Default response model returning only data."""

    data: DataT | None = Field(None, description="Primary data.")


class DataListResponse(BaseModel, Generic[DataT]):
    """Default response model returning only data."""

    data: list[DataT] | None = Field(None, description="Primary data.")


class DataValueResponse(BaseModel, Generic[ValueT]):
    """Default response model returning a single value as data."""

    data: ValueT | None = Field(None, description="Value")


class SuccessAndMessage(BaseModel):
    """Success and message for response."""

    success: bool = True
    message: str | None = Field(default="Success!")


class EmptyDefaultResponse(SuccessAndMessage):
    """Default response model with no data."""

    data: None = Field(default=None)


class OrmBasicModel(BaseModel):
    """Pydantic model to be created from an orm."""

    model_config = ConfigDict(from_attributes=True)


class DefaultResponse(SuccessAndMessage, Generic[DataT]):
    """Default response model."""

    data: DataT | None = Field(None, description="Primary data.")
