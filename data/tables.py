import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey, select, DateTime, update
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    
    def select_page_stmt(self):
        return select(type(self)).limit(5)

class Content(Base):
    __tablename__ = 'content'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.id'))
    subscription_id: Mapped[UUID] = mapped_column(ForeignKey('subscriptions.id'))
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True)
    length: Mapped[int] = mapped_column()
    publish_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    timestamp: Mapped[int] = mapped_column()
    finished: Mapped[bool] = mapped_column()

    def upsert_stmt(self):
        stmt = insert(Content).values(group_id=self.group_id, subscription_id=self.subscription_id, title=self.title, url=self.url, length=self.length, publish_date=self.publish_date)
        return stmt.on_conflict_do_update(
            index_elements=[Content.url],
            set_ = {'url': stmt.excluded.url}
        )
    
    def update_progress(self):
        return update(Content).values(timestamp=self.timestamp, finished=self.finished).where(id=self.id)  

    def select_by_value_stmt(self, title):
        return select(Content).where(Content.title == title)
    
    def select_page_stmt(self, subscription_id, limit=20, offset=0):
        return select(type(self)).where(Content.subscription_id == subscription_id).limit(limit).offset(offset).order_by(Content.publish_date.desc())


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, unique=True)

    def upsert_stmt(self):
        stmt = insert(Group).values(name=self.name)
        return stmt.on_conflict_do_update(
            index_elements=[Group.name],
            set_ = {'name': stmt.excluded.name}
        )
    
    def select_by_value_stmt(self, name):
        return select(Group).where(Group.name == name)
    
    def select_page_stmt(self, limit=20, offset=0):
        return select(self).limit(limit).offset(offset)


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.id'))
    feed_url: Mapped[str] = mapped_column(unique=True)
    last_item_date: Mapped[datetime.datetime] = mapped_column(DateTime)

    def upsert_stmt(self):
        stmt = insert(Subscription).values(title=self.title, group_id=self.group_id, feed_url=self.feed_url)
        return stmt.on_conflict_do_update(
            index_elements=[Subscription.feed_url],
            set_ = {'feed_url': stmt.excluded.feed_url}
        )
    
    def update_most_recent(self):
        return update(Subscription).values(last_item_date=self.last_item_date).where(id=self.id)

    def select_by_value_stmt(self, id):
        return select(Subscription).where(Subscription.id == id)
    
    def select_page_stmt(self, limit=20, offset=0):
        return select(type(self)).limit(limit).offset(offset)