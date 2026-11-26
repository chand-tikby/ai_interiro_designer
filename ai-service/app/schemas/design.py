from typing import Optional, List
from pydantic import BaseModel, Field


class RoomDesignRequest(BaseModel):
    room_type: str = Field(..., example="living_room", description="Type of room (e.g. living_room, bedroom, kitchen)")
    style: str = Field(..., example="minimalist", description="Desired style (e.g. minimalist, modern, scandinavian, industrial)")
    prompt: Optional[str] = Field(None, example="Add wooden accents, ambient warm lighting, and indoor plants")
    color_palette: Optional[List[str]] = Field(default=[], example=["#FFFFFF", "#D2B48C", "#4A5D4E"])
    budget_level: Optional[str] = Field(default="moderate", example="moderate")


class DesignRecommendation(BaseModel):
    category: str
    item_name: str
    suggested_color: str
    notes: Optional[str] = None


class RoomDesignResponse(BaseModel):
    status: str
    message: str
    design_id: Optional[str] = None
    style: str
    room_type: str
    recommendations: List[DesignRecommendation] = []
    generated_image_url: Optional[str] = None

