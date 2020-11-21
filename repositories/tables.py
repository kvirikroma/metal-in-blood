import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, Index, Boolean, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    def __repr__(self):
        if len(self.login) > 36:
            return self.login[:36] + '…'
        return self.login

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    login = Column(String(32), nullable=False, unique=True)
    email = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(64), nullable=False)

    admin = Column(Boolean(), nullable=False, default=False)
    change_tips = Column(Boolean(), nullable=False, default=False)
    change_news = Column(Boolean(), nullable=False, default=False)
    change_compilations = Column(Boolean(), nullable=False, default=False)
    language = Column(SmallInteger(), nullable=False, default=0)

    news_posts = relationship("NewsPost", backref='users', cascade='delete')
    forum_threads = relationship("ForumThread", backref='users', cascade='delete')
    forum_messages = relationship("ForumMessage", backref='users', cascade='delete')


class NewsPost(Base):
    __tablename__ = 'news'

    def __repr__(self):
        if len(self.title) > 36:
            return self.title[:36] + '…'
        return self.title

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(64), nullable=False)
    body = Column(String(8192), nullable=False)
    date = Column(DateTime(), nullable=False)
    picture = Column(String(512))

    user = relationship("User", back_populates="news", foreign_keys=[author])

    news_title_date_author_body_idx = Index('news_title_date_author_body_idx', title, date, author, body)


class Tip(Base):
    __tablename__ = 'tips'

    def __repr__(self):
        if len(self.title) > 36:
            return self.title[:36] + '…'
        return self.title

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(64), nullable=False, unique=True)
    body = Column(String(8192), nullable=False)
    picture = Column(String(512))
    tips_title_body_idx = Index('tips_title_body_idx', title, body)


class Album(Base):
    __tablename__ = 'albums'

    def __repr__(self):
        author = self.author
        name = self.album_name
        if len(author) > 12:
            author = author[:12] + '…'
        if len(name) > 16:
            name = name[:16] + '…'
        return f"{author} - {name}"

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(String(256), nullable=False)
    album_name = Column(String(256), nullable=False)
    picture = Column(String(512), unique=True, nullable=False)
    unique_index = UniqueConstraint('author', 'album_name', name='albums_author_album_name_key')


class YTCompilation(Base):
    __tablename__ = 'yt_compilations'

    def __repr__(self):
        if len(self.link) > 36:
            return self.link[:36] + '…'
        return self.link

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    link = Column(String(256), unique=True, nullable=False)
    channel = Column(String(256), nullable=False)
    video_name = Column(String(512), nullable=False)
    unique_index = UniqueConstraint('channel', 'video_name', name='yt_compilations_channel_video_name_key')


class ForumThread(Base):
    __tablename__ = 'forum_threads'

    def __repr__(self):
        if len(self.title) > 36:
            return self.title[:36] + '…'
        return self.title

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(64), nullable=False)
    body = Column(String(8192), nullable=False)
    date = Column(DateTime(), nullable=False)

    user = relationship("User", back_populates="forum_threads", foreign_keys=[author])

    threads = relationship("ForumMessage", backref='forum_threads', cascade='delete')

    forum_threads_author_title_key = UniqueConstraint('author', 'title', name='forum_threads_author_title_key')
    forum_threads_title_body_idx = Index('forum_threads_title_body_date_idx', title, body, date)
    forum_messages_related_to_fkey = relationship("ForumMessage", backref='forum_threads')


class ForumMessage(Base):
    __tablename__ = 'forum_messages'

    def __repr__(self):
        author = self.author
        related_to = self.related_to
        if len(author) > 12:
            author = author[:12] + '…'
        if len(related_to) > 12:
            related_to = related_to[:12] + '…'
        return f"{author}'s response to {related_to}"

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    body = Column(String(8192), nullable=False)
    date = Column(DateTime(), nullable=False)
    related_to = Column(UUID(), ForeignKey('forum_threads.id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", back_populates="forum_messages", foreign_keys=[author])
    thread = relationship("ForumThread", back_populates="forum_messages", foreign_keys=[related_to])

    forum_messages_related_to_idx = Index('forum_messages_related_to_idx', related_to)
