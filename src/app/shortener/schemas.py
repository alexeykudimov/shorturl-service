from pydantic import BaseModel


class FullLinkOut(BaseModel):
    full_link: str


class ShortenLinkOut(BaseModel):
    shorten_link: str
    