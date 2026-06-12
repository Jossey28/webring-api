from pathlib import Path
from typing import Any

from sqlmodel import (
    Field,
    create_engine,
    select,
    Session,
    SQLModel,
    JSON,
)


class Member(SQLModel):
    index: int
    owner: str
    site: str


class Ring(SQLModel, table=True):
    __tablename__: str = "rings-table"  # type: ignore

    id: int | None = Field(
        default=None, primary_key=True
    )  # https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#none-fields-nullable-columns; Set to null because database generates it, not code

    ring_name: str = Field(index=True)
    members: list[dict[str, Any]] = Field(default_factory=list, sa_type=JSON)


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
            Ring(
                ring_name="main",
                members=[
                    Member(
                        index=1,
                        owner="Jossey28",
                        site="https://dev-site.homecamp.biz",
                    ).model_dump(),
                    Member(
                        index=2,
                        owner="Sir Exemplaris",
                        site="https://example.com",
                    ).model_dump(),
                    Member(
                        index=3,
                        owner="Satya Nadella",
                        site="https://www.microsoft.com",
                    ).model_dump(),
                    Member(
                        index=4,
                        owner="Sundar Pichai",
                        site="https://google.com",
                    ).model_dump(),
                    Member(
                        index=5,
                        owner="Steve Jobs",
                        site="https://apple.com",
                    ).model_dump(),
                    Member(
                        index=6,
                        owner="John Ternus",
                        site="https://apple.com",
                    ).model_dump(),
                ],
            )
        )

        session.add(
            Ring(
                ring_name="upcoming",
                members=[
                    Member(
                        index=1,
                        owner="Jossey28",
                        site="https://dev-site.homecamp.biz",
                    ).model_dump(),
                    Member(
                        index=2,
                        owner="John Ternus",
                        site="https://apple.com",
                    ).model_dump(),
                ],
            )
        )

        session.add(
            Ring(
                ring_name="Apple",
                members=[
                    Member(
                        index=1,
                        owner="Steve Jobs",
                        site="https://apple.com",
                    ).model_dump(),
                    Member(
                        index=2,
                        owner="John Ternus",
                        site="https://apple.com",
                    ).model_dump(),
                ],
            )
        )

        session.commit()


def get_db_session():
    with Session(engine) as session:
        yield session


def get_all_members(ring_name: str) -> list[Ring]:
    with Session(engine) as session:
        result = list(session.exec(select(Ring)).all())
        return result
