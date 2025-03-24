import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, select, DateTime
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Content(Base):
    __tablename__ = 'content'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.id'))
    subscription_id: Mapped[UUID] = mapped_column(ForeignKey('subscriptions.id'))
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True)
    length: Mapped[int] = mapped_column()
    publish_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    def insert_stmt(self):
        stmt = insert(Content).values(group_id=self.group_id, subscription_id=self.subscription_id, title=self.title, url=self.url, length=self.length, publish_date=self.publish_date)
        return stmt.on_conflict_do_update(
            index_elements=[Content.url],
            set_ = {'url': stmt.excluded.url}
        )
    
    def select_stmt(self):
        return select(Content).where(Content.title == self.title)


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
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

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    content_id: Mapped[UUID] = mapped_column(ForeignKey('content.id'))
    timestamp: Mapped[int] = mapped_column()
    finished: Mapped[bool] = mapped_column()

    def insert_stmt(self):
        stmt = insert(PlayedContent).values(content_id=self.content_id, timestamp=self.timestamp, finished=self.finished)
        return stmt.on_conflict_do_update(
            index_elements=[PlayedContent.content_id],
            set_ = {'content_id': stmt.excluded.content_id}
        )
    
    def select_stmt(self):
        return select(PlayedContent).where(PlayedContent.content_id == self.content_id)

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.id'))
    feed_url: Mapped[str] = mapped_column(unique=True)

    def insert_stmt(self):
        stmt = insert(Subscription).values(title=self.title, group_id=self.group_id, feed_url=self.feed_url)
        return stmt.on_conflict_do_update(
            index_elements=[Subscription.feed_url],
            set_ = {'feed_url': stmt.excluded.feed_url}
        )
    
    def select_stmt(self):
        return select(Subscription).where(Subscription.id == self.id)