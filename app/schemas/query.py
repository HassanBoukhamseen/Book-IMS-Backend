from pydantic import BaseModel

class UserMessage(BaseModel):
    user_message: str