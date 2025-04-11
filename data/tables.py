from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey, select, DateTime, update, delete
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
    length: Mapped[int] = mapped_column(nullable=True)
    publish_date: Mapped[datetime] = mapped_column(DateTime)
    timestamp: Mapped[int] = mapped_column(nullable=True)
    finished: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return '''
{date} - {title}
{url}
Started: {started}
        '''.format(date=self.publish_date, title=self.title, url=self.url, started=self.timestamp is not None)

    def upsert_stmt(self):
        stmt = insert(Content).values(group_id=self.group_id, subscription_id=self.subscription_id, title=self.title, url=self.url, length=self.length, publish_date=self.publish_date)
        return stmt.on_conflict_do_update(
            set_ = {'length': stmt.excluded.length}
        )
    
    def upsert_bulk_stmt(self, values):
        stmt = insert(Content).values(list(values))
        return stmt.on_conflict_do_update(
            set_ = {'length': stmt.excluded.length}
        )
    
    def update_progress(self):
        return update(Content).values(timestamp=self.timestamp, finished=self.finished).where(url=self.url)  

    def select_by_value_stmt(title):
        return select(Content).where(Content.title == title)
    
    def select_by_subscription_stmt(subscription_id):
        return select(Content).where(Content.subscription_id == subscription_id).order_by(Content.publish_date.desc())

    def select_page_stmt(self, subscription_id, limit=20, offset=0):
        return select(Content).where(Content.subscription_id == subscription_id).limit(limit).offset(offset).order_by(Content.publish_date.desc())
    
    def delete_by_ids_stmt(self, group_id, subscription_id):
        return delete(Content).where(Content.group_id == group_id and Content.subscription_id == subscription_id)
    
    @staticmethod
    def sort(obj):
        return obj.publish_date

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
    
    def select_by_value_stmt(name):
        return select(Group).where(Group.name == name)
    
    def select_page_stmt(self, limit=20, offset=0):
        return select(Group).limit(limit).offset(offset)
    
    def delete_stmt(self, name):
        return delete(Group).where(Group.name == name).returning(Group.id)

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.id'))
    feed_url: Mapped[str] = mapped_column(unique=True)
    last_item_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __str__(self):
        return '{title}: {feed_url}'.format(title=self.title, feed_url=self.feed_url)

    def upsert_stmt(self):
        stmt = insert(Subscription).values(title=self.title, group_id=self.group_id, feed_url=self.feed_url, last_item_date=self.last_item_date)
        return stmt.on_conflict_do_update(
            index_elements=[Subscription.feed_url],
            set_ = {'title': stmt.excluded.title, 'feed_url': stmt.excluded.feed_url, 'last_item_date': stmt.excluded.last_item_date}
        )
    
    def update_most_recent(self):
        return update(Subscription).values(last_item_date=self.last_item_date).where(id=self.id)

    def select_by_value_stmt(url):
        return select(Subscription).where(Subscription.feed_url == url)
    
    def select_page_stmt(self, limit=20, offset=0):
        return select(Subscription).limit(limit).offset(offset)

    def delete_stmt(self, feed_url):
        return delete(Subscription).where(Subscription.feed_url == feed_url).returning(Subscription.id, Subscription.group_id)

    
class UserSettings(Base):
    __tablename__ = 'user_settings'

    id: Mapped[str] = mapped_column(primary_key=True, default='user', unique=True)
    auto_sync: Mapped[bool] = mapped_column(default=False)
    volume: Mapped[float] = mapped_column(default=0.5)
    display_images: Mapped[bool] = mapped_column(default=True)

    def upsert_stmt():
        stmt = insert(UserSettings).values()
        return stmt.on_conflict_do_nothing()

    def update_settings(self):
        return update(UserSettings).values(auto_sync=self.auto_sync, volume=self.volume, display_images=self.display_images)

    def select_by_value_stmt(user_id):
        return select(UserSettings).where(UserSettings.id == user_id)