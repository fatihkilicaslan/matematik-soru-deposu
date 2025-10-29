from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SoruModel(BaseModel):
    id: Optional[int] = None
    original_image: str
    cropped_image: Optional[str] = None
    soru_text: Optional[str] = None
    cevap: Optional[str] = None
    kategori_id: Optional[int] = None
    zorluk_seviyesi: int = 1
    detection_confidence: Optional[float] = None
    status: str = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class KategoriModel(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

class CevapRequest(BaseModel):
    soru_text: str
    cevap: str
    kategori_id: int
    zorluk_seviyesi: int = 1

class SoruResponse(BaseModel):
    success: bool
    message: str
    questions: Optional[List[dict]] = None