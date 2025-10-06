"""RFC 7807 Problem Details model definition."""

from pydantic import AnyUrl, BaseModel


class Problem(BaseModel):
    """RFC 7807 Problem Details object for HTTP error responses."""

    type: AnyUrl | None = None
    title: str
    status: int
    detail: str | None = None
    instance: AnyUrl | None = None

    class Config:
        """Pydantic model config."""

        extra = "allow"  # позволяем доп.поля по RFC 7807/9457
