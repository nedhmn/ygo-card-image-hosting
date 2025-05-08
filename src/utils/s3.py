import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aioboto3
from types_aiobotocore_s3.client import S3Client

from src.config import Settings

logger = logging.getLogger(__name__)


class AsyncS3Client:
    def __init__(self, bucket_name: str, s3_client: S3Client):
        self.bucket_name = bucket_name
        self.s3_client = s3_client

    async def put_object(self, key: str, body: bytes, content_type: str) -> None:
        await self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=body,
            ContentType=content_type,
        )
        logger.info("Successfully uploaded object with key: %s", key)

    async def list_keys(self) -> list[str]:
        keys: list[str] = []
        paginator = self.s3_client.get_paginator("list_objects_v2")

        async for page in paginator.paginate(Bucket=self.bucket_name):
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])

        return keys


@asynccontextmanager
async def get_async_s3_client(
    settings: Settings,
) -> AsyncGenerator[AsyncS3Client, None]:
    session = aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    async with session.client("s3") as s3_client:
        yield AsyncS3Client(settings.BUCKET_NAME, s3_client)
