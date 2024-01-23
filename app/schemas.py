from pydantic import BaseModel

class Quote(BaseModel):
    quote: str
    anime: str
    character: str

    class Config:
        from_attributes = True