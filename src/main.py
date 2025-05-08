import asyncio
import functools
import logging

import aiometer
import httpx

from src.config import settings
from src.utils.logging import setup_logger
from src.utils.s3 import AsyncS3Client, get_async_s3_client
from src.utils.types import YPDResponse

setup_logger("main.log")
logger = logging.getLogger("main")


async def ygo_card_seeder() -> None:
    logger.info("Starting YGO card seeder...")
    async with (
        httpx.AsyncClient() as http_client,
        get_async_s3_client(settings) as s3_client,
    ):
        # Get card urls
        card_urls = await get_card_urls_to_upload(http_client, s3_client)
        logger.info("Retrieved %s card URLs", len(card_urls))

        if not card_urls:
            logger.info("All card images are already in S3!")
            return

        # Upload cards to s3
        logger.info("Uploading card images to S3...")
        await aiometer.run_on_each(
            async_fn=functools.partial(
                upload_card_to_s3, http_client=http_client, s3_client=s3_client
            ),
            args=card_urls,
            max_per_second=settings.AIOMETER_MAX_PER_SECOND,
            max_at_once=settings.AIOMETER_MAX_AT_ONCE,
        )
        logger.info("Card image upload tasks completed")


async def get_card_urls_to_upload(
    http_client: httpx.AsyncClient, s3_client: AsyncS3Client
) -> list[str]:
    # Get current cards from s3
    s3_image_keys = await s3_client.list_keys()
    logger.info("Found %s image keys in S3", len(s3_image_keys))

    # Get all cards from ygoprodeck within date range
    card_image_urls = await get_card_image_urls(http_client)
    logger.info("Found %s card image URLs from YGOPRODECK", len(card_image_urls))

    if not s3_image_keys:
        return card_image_urls

    # Return cards that aren’t already in s3
    s3_keys_set = set(s3_image_keys)
    filtered_urls = [url for url in card_image_urls if url not in s3_keys_set]

    logger.info("%s new card image URLs to upload", len(filtered_urls))
    return filtered_urls


async def get_card_image_urls(http_client: httpx.AsyncClient) -> list[str]:
    # Get cards from ygoprodeck
    response = await http_client.get(settings.YGOPRODECK_URL)
    response.raise_for_status()

    # Return only the `image_url` from each card_images entry
    data: YPDResponse = response.json()
    image_urls = [
        image[settings.CARD_IMAGE_KEY]
        for card in data.get("data", [])
        for image in card.get("card_images", [])
        if settings.CARD_IMAGE_KEY in image
    ]
    return image_urls


async def upload_card_to_s3(
    url: str, http_client: httpx.AsyncClient, s3_client: AsyncS3Client
) -> None:
    # Prefix validation
    prefix = "https://images.ygoprodeck.com/"
    if not url.startswith(prefix):
        logger.warning("URL %s did not start with the correct prefix", url)
        return

    # Download the card image
    response = await http_client.get(url)
    response.raise_for_status()

    # Get the image bytes and content type
    body = response.content
    content_type = response.headers.get("Content-Type")

    if content_type != "image/jpeg":
        logger.warning("URL %s had an invalid Content-Type", url)
        return

    # Remove prefix to get s3 key
    s3_key = url[len(prefix) :]

    # Upload the image to S3.
    await s3_client.put_object(s3_key, body, content_type)
    logger.info(f"Successfully uploaded image to S3 with key: {s3_key}")


if __name__ == "__main__":
    asyncio.run(ygo_card_seeder())
