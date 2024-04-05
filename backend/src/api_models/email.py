from pydantic import BaseModel


class ChallengeEmail(BaseModel):
    send_to_username: str
    send_to_email: str
    sent_from_username: str
