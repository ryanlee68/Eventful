from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker as maker
from tables import Attendance, Codes, mapper
from fastapi import FastAPI, HTTPException, status, Depends
from test import make_event
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordReqeustForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from pydantic import BaseModel
from auth import get_Attendee, get_ClubAccount, authenticateAttendee, authenticateClubAccount, create_access_token
from jwtF import verify_password, get_password_hash
import aiohttp

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
# from . import config

# from .logs import setUpLogger, set_pretty_formatter, logs_dir, PrettyFormatter

# set_pretty_formatter('%(levelname)s | %(name)s: %(asctime)s - [%(funcName)s()] %(message)s')
# # ADD ELEMENTS TO THE ARRAY BELOW AS WEL ADD NEW FILES
# for name in ['app']:
#     setUpLogger(f'ucmbot.{name}', files=not config.testing)

app = FastAPI()

# engine = create_async_engine("sqlite+aiosqlite:///:memory:")
engine = create_async_engine("sqlite+aiosqlite:///api.db")
        
@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(mapper.metadata.create_all)

sessionmaker = maker(bind=engine, class_=AsyncSession)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenDataAttendee(BaseModel):
    studentID: Optional[str] = None

class TokenDataClubAccount(BaseModel):
    clubID: Optional[str] = None

class UserInDB(Attendee):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

async def create_user(studentID, password):
    newAttendee = ''
    async with sessionmaker.begin() as session:
        user = session.get(Attendee, studentID)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user already exists in the system",
            )
        newAttendee: Attendee = Attendee(studentID = studentID, hashed_password = get_password_hash(password))
        session.add(newAttendee)
    return newAttendee

async def create_user(clubID, password):
    newAttendee = ''
    async with sessionmaker.begin() as session:
        user = session.get(ClubAccount, clubID)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The club already exists in the system",
            )
        newAttendee: ClubAccount = ClubAccount(studentID = studentID, hashed_password = get_password_hash(password))
        session.add(newAttendee)
    return newAttendee


async def get_current_Attendee(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        studentID: str = payload.get("sub")
        if studentID is None:
            raise credentials_exception
        token_data = TokenDataAttendee(studentID=studentID)
    except JWTError:
        raise credentials_exception
    user = get_Attendee(token_data.studentID)
    if user is None:
        raise credentials_exception
    return user
    
async def get_current_ClubAccount(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        clubID: str = payload.get("sub")
        if studentID is None:
            raise credentials_exception
        token_data = TokenDataClubAccount(clubID=clubID)
    except JWTError:
        raise credentials_exception
    user = get_ClubAccount(token_data.clubID)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_Attendee(current_user: Attendee = Depends(get_current_Attendee)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_ClubAccount(current_user: ClubAccount = Depends(get_current_ClubAccount)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def check_valid_id(stuid, code):
    # check what meeting code is part of
    # do to icatcard and submit

@app.post("/attendee-token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticateAttendee(form_data.studentID, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.studentID}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/clubAccount-token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticateClubAccount(form_data.clubID, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.clubID}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/attendees/me/", response_model=Attendee)
async def read_users_me(current_user: Attendee = Depends(get_current_active_Attendee)):
    return current_user

@app.get("/clubAccounts/me/", response_model=ClubAccount)
async def read_users_me(current_user: Attendee = Depends(get_current_active_ClubAccount)):
    return current_user

@app.post("/submit_attendance")
async def submit_attendance(stuid:int, code:int):
    async with sessionmaker.begin() as session:
        # session: AsyncSession = session
        codes = await session.get(Codes, code)
        if not codes:
            raise HTTPException(status_code=404, detail="Code not found")
        elif not await check_valid_id(stuid, code):
            raise HTTPException(status_code=403, detail="ID not valid")
        elif await session.get(Attendance, [stuid, code]):
            raise HTTPException(status_code=400, detail="Duplicate student ID and code")
        else:
            # instance: Attendance = Attendance(student_id=stuid, code=code)
            instance: Attendance = Attendance(stuid, code)
            session.add(instance)

    return {"Success": "ok"}

@app.get("/get-clubs")
async def get_clubs():
    async with aiohttp.request("get", "https://api.presence.io/ucmerced/v1/organizations/") as request:
        file = await request.json()
    names = [i['name'] for i in file]
    print(names)

@app.post("/get_code")
async def get_code(username:str, password:str):
    # first, check if username and password is in database, if not, check if username and pasword is valid
    async with sessionmaker.begin() as session:
        user = await session.get(Auth, username)
        passwd = await session.get(Auth, password)
        if(not user or passwd):
            # check if they are actuall correct by using aiohttp function
                # if true 
                    #add user and passwd to the Auth table
                    #---------------
                    # now the event registeration function that runs all the time will get the club name and 
                    #search for the latest event of that club in the presence api and using that event's data, it will 
                    #create the event in iCheck-in after it signs in the icatcard system using clubID and password, and if succesful it will generate the code and put that in the codes table
                    #---------------
                    # go to codes table and find the code associated with the clubID
                    # return that code
                # if not true 
                    # return a message saying wrong username or password
        #go to codes table and return the code that is already generated for that club