from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker as maker
from tables import Attendance, Codes, mapper
from fastapi import FastAPI, HTTPException
from test import make_event

import asyncio
import aiohttp

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def check_valid_id(stuid, code):
    # check what meeting code is part of
    # do to icatcard and submit

@app.post("/submit-attendance")
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

@app.post("/get-code")
async def get_code(username:str, password:str):
    # first, check if username and password is in database, if not, check if username and pasword is valid
    async with sessionmaker.begin() as session:
        user = await session.get(Auth, username)
        passwd = await session.get(Auth, password)
        if(not user or passwd):
            # check if they are actuall correct by using aiohttp function
            # add user and passwd to the Auth table
        #go to codes table 