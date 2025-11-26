from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
    Dict,
    Union
)

from pydantic import BaseModel, Field, ConfigDict


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int

class UserRole(str, Enum):
    "[Guest, Player, Administrator, NannyModerator, RegularModerator, SeniorModerator]"
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'Nanny Moderator'
    REGULAR_MODERATOR = 'Regular Moderator'
    SENIOR_MODERATOR = 'Senior Moderator'

class BbParseMode(str, Enum):
    '[Common, Info, Post, Chat]'
    COMMON = 'COMMON'
    INFO = 'INFO'
    POST = 'POST'
    CHAT = 'CHAT'

class PagingSettings(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')

class ColorSchema(list, Enum):
    '[ Modern, Pale, Classic, ClassicPale, Night ]'
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSICPALE = 'ClassicPale'
    NIGHT = 'Night'

class UserSettings(BaseModel):
    color_schema: Optional[List[ColorSchema]] = Field(None, serialization_alias='colorSchema')
    nanny_greetings_message: Optional[str] = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings

class InfoBbText(BaseModel):
    value: Optional[str] = None
    parse_mode: Optional[List[BbParseMode]] = Field(None, serialization_alias='parseMode')

class UserDetails(BaseModel):
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
    icq: str = Field(None, alias='icq')
    skype: str = Field(None, alias='skype')
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: Optional[Union[InfoBbText, str]] = Field(None, alias='info')
    settings: Optional[UserSettings]


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
    #type: #Optional[str] = Field(None, description='Type')
    #title: Optional[str] = Field(None, description='Title')
    #status: Optional[int] = Field(None, description='Status code')
    #traceId: Optional[str] = Field(None, description='traceId')