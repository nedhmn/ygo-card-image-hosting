import asyncio
import logging

import aiometer
import httpx

from src.config import settings
from src.utils.logging import setup_logger
from src.utils.s3 import AsyncS3Client, get_async_s3_client
from src.utils.types import YPDResponse

setup_logger("src/main.log")
logger = logging.getLogger("main")


async def ygo_card_seeder() -> None:
    async with (
        httpx.AsyncClient() as http_client,
        get_async_s3_client(settings) as s3_client,
    ):
        # Get card urls
        card_urls = await get_card_urls_to_upload(http_client, s3_client)

        if not card_urls:
            logger.info("All card images are already in s3!")
            return


async def get_card_urls_to_upload(
    http_client: httpx.AsyncClient, s3_client: AsyncS3Client
) -> list[str]:
    # Get current cards from s3
    s3_image_keys = await s3_client.list_keys()

    # Get all cards from ygoprodeck within date range
    card_image_urls = await get_card_image_urls(http_client)

    if not s3_image_keys:
        return card_image_urls

    # Return cards that aren't already in s3
    s3_keys_set = set(s3_image_keys)
    return [url for url in card_image_urls if url not in s3_keys_set]


async def get_card_image_urls(http_client: httpx.AsyncClient) -> list[str]:
    # Get cards from ygoprodeck
    response = await http_client.get(settings.YGOPRODECK_URL)
    data: YPDResponse = response.json()

    # Return only the `image_url` from each card_images entry
    return [
        image["image_url"]
        for card in data.get("data", [])
        for image in card.get("card_images", [])
        if "image_url" in image
    ]


async def upload_card_to_s3() -> None:
    pass


if __name__ == "__main__":
    asyncio.run(ygo_card_seeder())
