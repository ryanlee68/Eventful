from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from tables import Attendee, ClubAccount
from security import verify_password

import database as _database, models as _models, schemas as _schemas

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def get_Attendee(studentID):
    async with sessionmaker.begin() as session:
        attendee = await session.get(Attendee, studentID)
        return attendee

def get_ClubAccount(clubID):
        async with sessionmaker.begin() as session:
        clubAcc = await session.get(ClubAccount, clubID)
        return clubAcc

def authenticateAttendee(
    *,
    studentID: str,
    password: str,
) -> Optional[Attendee]:
    user = get_Attendee(studentID)
    if not user:
        return None
    if not verify_password(password, Attendee.hashed_password):
        return None
    return user

def authenticateClubAccount(
    *,
    clubID: str,
    password: str,
) -> Optional[ClubAccount]:
    user = get_ClubAccount(clubID)
    if not user:
        return None
    if not verify_password(password, ClubAccount.hashed_password):
        return None
    return user

def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )

def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

