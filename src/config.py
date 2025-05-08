from datetime import datetime
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # YGOPRODECK
    START_DATE: str = Field(
        description="The start release date for the YGO cards to add to s3."
    )
    END_DATE: str = Field(
        description="The end release date for the YGO cards to add to s3."
    )

    @field_validator("START_DATE", "END_DATE", mode="after")
    @classmethod
    def ensure_correct_date_fmt(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError(f"{value} must be in format YYYY-MM-DD")

    DATE_REGION: Literal["tcg", "ocg"] = Field(default="tcg")

    # AWS
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str


settings = Settings()
