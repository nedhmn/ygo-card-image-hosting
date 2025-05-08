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
        default="2002-03-01",
        description="The start release date for the YGO cards to add to s3.",
    )
    END_DATE: str = Field(
        default="2002-04-01",
        description="The end release date for the YGO cards to add to s3.",
    )

    # Custom field validation
    # ref: https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator
    @field_validator("START_DATE", "END_DATE", mode="after")
    @classmethod
    def ensure_correct_date_fmt(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError(f"{value} must be in format YYYY-MM-DD")

    DATE_REGION: Literal["tcg", "ocg"] = Field(default="tcg")

    @property
    def YGOPRODECK_URL(self) -> str:
        # Create ygoprodeck url
        return (
            "https://db.ygoprodeck.com/api/v7/cardinfo.php?"
            f"startdate={self.START_DATE}&"
            f"enddate={self.END_DATE}&"
            f"dateregion={self.DATE_REGION}"
        )

    CARD_SIZE: Literal["FULL", "SMALL", "CROPPED"] = Field(
        default="FULL", description="Card image size to upload to s3."
    )

    @property
    def CARD_IMAGE_KEY(
        self,
    ) -> Literal["image_url", "image_url_small", "image_url_cropped"]:
        """The card_images key name for different card sizes from ygoprodeck's api."""
        if self.CARD_SIZE == "FULL":
            return "image_url"
        elif self.CARD_SIZE == "SMALL":
            return "image_url_small"
        else:
            return "image_url_cropped"

    # AWS
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str

    # Misc
    AIOMETER_MAX_PER_SECOND: int = Field(
        default=19,
        description="Maximum requests per second - rate limited by ygoprodeck at 20 per second.",
    )
    AIOMETER_MAX_AT_ONCE: int = Field(
        default=19, description="Maximum requests at once."
    )


settings = Settings()
