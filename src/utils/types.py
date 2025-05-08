from typing import Literal, TypedDict


class CardImage(TypedDict):
    id: int
    image_url: str
    image_url_small: str
    image_url_cropped: str


class Card(TypedDict, total=False):
    card_images: list[CardImage]


YPDResponse = dict[Literal["data"], list[Card]]
