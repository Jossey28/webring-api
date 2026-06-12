from pathlib import Path

from sqlalchemy import JSON, Column
from sqlmodel import Field, Session, create_engine, SQLModel


class Member(SQLModel, table=True):
    __tablename__: str = "members"  # type: ignore

    id: int | None = Field(
        default=None, primary_key=True
    )  # https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#none-fields-nullable-columns; Set to null because database generates it, not code
    index: int
    owner: str
    site: str

    rings: list[str] = Field(sa_column=Column(JSON))


def init_db(db_path: Path):
    db_url = f"sqlite:///{db_path.absolute()}"
    print(f"Using db_url: {db_url}")

    # Importing but not reading: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters
    from helpers.db import Member  # type: ignore

    global engine
    engine = create_engine(db_url, echo=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(
            Member(
                index=1,
                owner="Jossey28",
                site="https://dev-site.homecamp.biz",
                rings=["main", "upcoming"],
            )
        )

        session.add(
            Member(
                index=2,
                owner="Sir Exemplaris",
                site="https://example.com",
                rings=["main"],
            )
        )

        session.add(
            Member(
                index=3,
                owner="Satya Nadella",
                site="https://www.microsoft.com",
                rings=["main"],
            )
        )

        session.add(
            Member(
                index=4,
                owner="Sundar Pichai",
                site="https://google.com",
                rings=["main"],
            )
        )

        session.add(
            Member(
                index=5,
                owner="John Ternus",
                site="https://apple.com",
                rings=["main", "upcoming", "apple"],
            )
        )

        session.add(
            Member(
                index=6,
                owner="Steve Jobs",
                site="https://apple.com",
                rings=["main", "upcoming", "apple"],
            )
        )

        session.commit()


def get_db_session():
    with Session(engine) as session:
        yield session
