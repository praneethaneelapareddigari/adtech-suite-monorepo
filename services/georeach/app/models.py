from pydantic import BaseModel, Field
from typing import List, Tuple

class CampaignIn(BaseModel):
    campaign_id: str
    name: str
    polygon: List[Tuple[float, float]] = Field(..., description="List of [lon,lat] forming a closed ring")