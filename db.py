from sqlmodel import Field, SQLModel, create_engine,Session
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session