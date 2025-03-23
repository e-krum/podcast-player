import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, select, DateTime
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Content(Base):
    __tablename__ = 'content'

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True)
    length: Mapped[int] = mapped_column()
    publish_date: Mapped[datetime.datetime] = mapped_column(DateTime)


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    def insert_stmt(self):
        stmt = insert(Group).values(name=self.name)
        return stmt.on_conflict_do_update(
            index_elements=[Group.name],
            set_ = {'name': stmt.excluded.name}
        )
    
    def select_stmt(self):
        return select(Group).where(Group.name == self.name)

class PlayedContent(Base):
    __tablename__ = 'played_content'

    id: Mapped[int] = mapped_column(primary_key=True)
    content_id: Mapped[int] = mapped_column(ForeignKey('content.id'))
    timestamp: Mapped[int] = mapped_column()
    finished: Mapped[bool] = mapped_column()

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    feed_url: Mapped[str] = mapped_column(unique=True)