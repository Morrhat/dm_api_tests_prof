
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
    Union,
)

from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    "[Guest, Player, Administrator, NannyModerator, RegularModerator, SeniorModerator]"
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'Nanny Moderator'
    REGULAR_MODERATOR = 'Regular Moderator'
    SENIOR_MODERATOR = 'Senior Moderator'

class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias='online')
    name: str = Field(None, alias='name')
    location: str = Field(None, alias='location')
    registration: datetime = Field(None, alias='registration')


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[User] = None
    metadata: Optional[Union[dict, str]] = None






