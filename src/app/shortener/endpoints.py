import logging
from fastapi import APIRouter, Depends, HTTPException

from src.app.shortener.schemas import FullLinkOut, ShortenLinkOut
from src.app.shortener.service import ShortenerService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
        "", 
        status_code=201,
        response_model=ShortenLinkOut)
async def create_link(
        full_link: str,
        shortener_service: ShortenerService = Depends()):
    '''
    Create shorten link
    '''
    return await shortener_service.generate_shorten_link(full_link)

@router.get(
        "", 
        status_code=200,
        response_model=FullLinkOut)
async def retrieve_link(
        shorten_link: str,
        shortener_service: ShortenerService = Depends()):
    '''
    Retrieve full link by shorten
    '''
    return await shortener_service.retrieve_full_link(shorten_link)

@router.delete(
        "", 
        status_code=204)
async def delete_link(
        shorten_link: str,
        shortener_service: ShortenerService = Depends()):
    '''
    Delete shorten link
    '''
    return await shortener_service.delete_shorten_link(shorten_link)


