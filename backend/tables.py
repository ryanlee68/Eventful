from sqlalchemy import Column, BigInteger, Integer, String
from sqlalchemy.orm.decl_api import registry
from dataclasses import dataclass, field

mapper = registry()

@mapper.mapped
@dataclass
class Attendance:
    __tablename__ = 'attendance'

    __sa_dataclass_metadata_key__ = 'sa'

    student_id: int = field(metadata={
        'sa': Column(BigInteger, primary_key=True)
    })
    code: int = field(metadata={
        'sa': Column(Integer, primary_key=True)
    })

@mapper.mapped
@dataclass
class Codes:
    __tablename__ = 'codes'

    __sa_dataclass_metadata_key__ = 'sa'

    codes: int = field(metadata={
        'sa': Column(Integer, primary_key=True)
    })

@mapper.mapped
@dataclass
class Attendee:
    __tablename__ = 'auth'

    __sa_dataclass_metadata_key__ = 'sa'

    studentID: str = field(metadata={
        'sa': Column(String, primary_key=True)
    })
    password: str = field(metadata={
        'sa': Column(String, primary_key=True)
    })
    points: int = field(metadata={
        'sa': Column(Integer, primary_key=False)
    })
    hashed_password = Column(String, nullable=False)

@mapper.mapped
@dataclass
class ClubAccount:
    __tablename__ = 'auth'

    __sa_dataclass_metadata_key__ = 'sa'

    clubID: str = field(metadata={
        'sa': Column(String, primary_key=True)
    })
    password: str = field(metadata={
        'sa': Column(String, primary_key=True)
    })
    hashed_password = Column(String, nullable=False)