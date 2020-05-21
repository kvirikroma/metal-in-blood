from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    def __repr__(self):
        return self.login

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    login = Column(String(64), nullable=False, unique=True)
    email = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(64), nullable=False)
    news_author_fkey = relationship("NewsPost", backref='users')
    forum_threads_author_fkey = relationship("ForumThread", backref='users')
    forum_messages_author_fkey = relationship("ForumMessage", backref='users')


class NewsPost(Base):
    __tablename__ = 'news'

    def __repr__(self):
        return self.title

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(64), nullable=False)
    body = Column(String(8192), nullable=False)
    date = Column(DateTime, nullable=False)
    picture = Column(String(512))
    news_title_date_author_body_idx = Index('news_title_date_author_body_idx', title, date, author, body)


class Tip(Base):
    __tablename__ = 'tips'

    def __repr__(self):
        return self.title

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(64), nullable=False, unique=True)
    body = Column(String(8192), nullable=False)
    picture = Column(String(512))
    tips_title_body_idx = Index('tips_title_body_idx', title, body)


class Album(Base):
    __tablename__ = 'albums'

    def __repr__(self):
        return self.author + " - " + self.album_name

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(String(256), nullable=False)
    album_name = Column(String(256), nullable=False)
    picture = Column(String(512), unique=True, nullable=False)
    unique_index = UniqueConstraint('author', 'album_name', name='albums_author_album_name_key')


class YTCompilation(Base):
    __tablename__ = 'yt_compilations'

    def __repr__(self):
        return self.link

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    link = Column(String(256), unique=True, nullable=False)
    channel = Column(String(256), nullable=False)
    video_name = Column(String(512), nullable=False)
    unique_index = UniqueConstraint('channel', 'video_name', name='yt_compilations_channel_video_name_key')


class ForumThread(Base):
    __tablename__ = 'forum_threads'

    def __repr__(self):
        return self.title

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(64), nullable=False)
    body = Column(String(8192), nullable=False)
    date = Column(DateTime, nullable=False)
    forum_threads_author_title_key = UniqueConstraint('author', 'title', name='forum_threads_author_title_key')
    forum_threads_title_body_idx = Index('forum_threads_title_body_idx', title, body)
    forum_messages_related_to_fkey = relationship("ForumMessage", backref='forum_threads')


class ForumMessage(Base):
    __tablename__ = 'forum_messages'

    def __repr__(self):
        return self.author + " response to " + self.related_to

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    body = Column(String(8192), nullable=False)
    date = Column(DateTime, nullable=False)
    related_to = Column(UUID(), ForeignKey('forum_threads.id', ondelete='CASCADE'), nullable=False)
    forum_messages_related_to_idx = Index('forum_messages_related_to_idx', related_to)
