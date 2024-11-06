# models.py
from enum import Enum
import json
from typing import Literal, List, Dict, Any, Optional, Union
from pydantic import BaseModel, HttpUrl, field_validator
from typing import List



class TranscriptRequest(BaseModel):
    token: str
    mediaURL: str


class TranscriptResponse(BaseModel):
    lang: str
    message: str
    success: bool
