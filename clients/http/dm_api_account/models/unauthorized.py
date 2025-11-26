from pydantic import BaseModel, Field, ConfigDict

class Unauthorized(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: str = Field(..., description='Type')
    title: str = Field(..., description='Title')
    status: int = Field(..., description='Status code')
    traceId: str = Field(..., description='traceId')