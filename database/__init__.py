from sqlalchemy import create_engine

engine = create_engine("sqlite:///frog.db", echo=True)
