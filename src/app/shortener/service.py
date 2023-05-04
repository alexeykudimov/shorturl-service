import logging
import string
import random

from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.misc.dependencies import get_async_session

from src.app.shortener.models import Link
from src.app.shortener.schemas import ShortenLinkOut, FullLinkOut

from src.config.settings import settings

logger = logging.getLogger(__name__)


class ShortenerService:
    def __init__(self,
                 db: AsyncSession = Depends(get_async_session)):
        self.db = db

    @staticmethod
    def get_shortened_id(link: str):
        return link.split('/')[-1]

    async def generate_shortened_id(self) -> str:
        shortened_id = ''.join(
                random.choices(string.ascii_letters + string.digits, k=settings.URL_TAIL_LENGTH))

        # if generated link already exists in db recursive generate another one
        stmt = select(Link).where(Link.shortened_id == shortened_id)
        link = (await self.db.execute(stmt)).scalar_one_or_none()
        
        if link:
            return self.generate_shortened_id()
        
        return shortened_id
    
    async def create_shorten_link(self, *args, **kwargs) -> Link:
        new_link = Link(**kwargs)
        self.db.add(new_link)
        await self.db.commit()

        return new_link
    
    async def generate_shorten_link(self, full_link: str) -> ShortenLinkOut:
        shortened_id = await self.generate_shortened_id()
        new_link = await self.create_shorten_link(
                shortened_id=shortened_id, full_link=full_link)
        
        return {"shorten_link": new_link.shortened_link}

    async def retrieve_full_link(self, shorten_link: str) -> FullLinkOut:
        shortened_id = self.get_shortened_id(shorten_link)

        stmt = select(Link).where(Link.shortened_id == shortened_id)
        shorten_link = (await self.db.execute(stmt)).scalar_one_or_none()

        if not shorten_link:
            raise HTTPException(status_code=404, detail="This link doesn't exist")

        return {"full_link": shorten_link.full_link}
    
    async def delete_shorten_link(self, shorten_link: str):
        shortened_id = self.get_shortened_id(shorten_link)

        stmt = delete(Link).where(Link.shortened_id == shortened_id)
        await self.db.execute(stmt)
        await self.db.commit()
