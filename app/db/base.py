from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import model modules here so migration tools can discover their metadata.
