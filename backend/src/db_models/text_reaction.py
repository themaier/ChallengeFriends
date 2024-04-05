from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TextReactionTable(SQLModel, table=True):
    __tablename__ = "text_reactions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    challenge_id: int
    text: Optional[str] = Field(default=None)
    image_path: Optional[str] = Field(default=None)