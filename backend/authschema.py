from pydantic import BaseModel


class AuthDetails(BaseModel):
    studentID: str
    password: str