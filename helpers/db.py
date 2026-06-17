from pathlib import Path
from typing import Any

from sqlalchemy import Column
from sqlmodel import (
    Field,
    create_engine,
    select,
    Session,
    SQLModel,
    JSON,
)

from fastapi import HTTPException, Request, status


class Member(SQLModel):
    index: int
    owner: str
    site: str
    eightyeight: str | None = Field(default=None)


class Ring(SQLModel, table=True):
    __tablename__: str = "rings-table"  # type: ignore

    id: int | None = Field(
        default=None, primary_key=True
    )  # https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#none-fields-nullable-columns; Set to null because database generates it, not code

    api_keys: list[str] | None = Field(default=None, sa_column=Column(JSON))

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
                ring_name="demo-sites",
                api_keys=["DKmWzG5AmVy67kGmzpoO14TeaUlFJNZK"],
                members=[
                    Member(
                        index=1,
                        owner="First Owner",
                        site="https://site-1.homecamp.biz",
                    ).model_dump(),
                    Member(
                        index=2,
                        owner="Second Owner",
                        site="https://site-2.homecamp.biz",
                    ).model_dump(),
                    Member(
                        index=3,
                        owner="Third Owner",
                        site="https://site-3.homecamp.biz",
                    ).model_dump(),
                ],
            )
        )

        session.commit()


def get_db_session():
    with Session(engine) as session:
        yield session


def get_all_members(request: Request, ring_name: str | None = None) -> list[Member]:
    with Session(engine) as session:
        ring = session.exec(
            select(Ring).where(Ring.ring_name == request.app.state.default_ring)
        ).first()

        if ring is not None and request.url.path == "/webring/all":
            memebers: list[Member] = list()
            for member in ring.members:
                memebers.append(Member.model_validate(member))
            return memebers

        ring = session.exec(select(Ring).where(Ring.ring_name == ring_name)).first()
        if ring is not None:
            memebers = [Member.model_validate(member) for member in ring.members]
            return memebers

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ring doesn't exist in database",
        )


def get_member_owner(request: Request, ring_name: str, owner: str) -> Member:
    with Session(engine) as session:
        ring = session.exec(select(Ring).where(Ring.ring_name == ring_name)).first()

        if ring is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ring doesn't exist in database",
            )

        members = [Member.model_validate(member) for member in ring.members]

        if len(members) == 0:
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail="This ring has no members"
            )

        if request.url.path.find("/next/owner/") != -1:
            get_next = True
        else:
            get_next = False

        members_iter = iter(members)
        prev = None
        for member in members_iter:
            if member.owner == owner:
                if get_next:
                    next_member = next(members_iter, None)
                    if next_member is not None:
                        return next_member
                    else:
                        return members[0]
                else:
                    if prev is not None:
                        return prev
                    else:
                        return members[-1]

            prev = member

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner doesn't exist in ring",
        )


def get_member_index(request: Request, ring_name: str, index: int) -> Member:
    with Session(engine) as session:
        ring = session.exec(select(Ring).where(Ring.ring_name == ring_name)).first()

        if ring is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ring doesn't exist in database",
            )

        members = [Member.model_validate(member) for member in ring.members]

        if len(members) == 0:
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail="This ring has no members"
            )

        if request.url.path.find("/next/index/") != -1:
            get_next = True
        else:
            get_next = False

        members_iter = iter(members)
        prev = None
        for member in members_iter:
            if member.index == index:
                if get_next:
                    next_member = next(members_iter, None)
                    if next_member is not None:
                        return next_member
                    else:
                        return members[0]
                else:
                    if prev is not None:
                        return prev
                    else:
                        return members[-1]

            prev = member

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Index doesn't exist in ring",
        )


def get_member_site(request: Request, ring_name: str, site: str) -> Member:
    with Session(engine) as session:
        ring = session.exec(select(Ring).where(Ring.ring_name == ring_name)).first()

        if ring is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ring doesn't exist in database",
            )

        members = [Member.model_validate(member) for member in ring.members]

        if len(members) == 0:
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail="This ring has no members"
            )

        if request.url.path.find("/next/site/") != -1:
            get_next = True
        else:
            get_next = False

        members_iter = iter(members)
        prev = None
        for member in members_iter:
            if member.site == site:
                if get_next:
                    next_member = next(members_iter, None)
                    if next_member is not None:
                        return next_member
                    else:
                        return members[0]
                else:
                    if prev is not None:
                        return prev
                    else:
                        return members[-1]

            prev = member

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site doesn't exist in ring",
        )
