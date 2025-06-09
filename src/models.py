from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relationships
    following: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.user_from_id',
        back_populates='follower_user'
    )
    followers: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.user_to_id',
        back_populates='followed_user'
    )
    posts: Mapped[list['Post']] = relationship('Post', back_populates='user_post')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user_comment')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    follower_user: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_from_id],
        back_populates='following'
    )
    followed_user: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_to_id],
        back_populates='followers'
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    user_post: Mapped['User'] = relationship('User', back_populates='posts')
    post_media: Mapped[list['Media']] = relationship('Media', back_populates='media_post')
    comment_post: Mapped[list['Comment']] = relationship('Comment', back_populates='post_comment')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    media_post: Mapped['Post'] = relationship('Post', back_populates='post_media')

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "post_id": self.post_id
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    user_comment: Mapped['User'] = relationship('User', back_populates='comments')
    post_comment: Mapped['Post'] = relationship('Post', back_populates='comment_post')

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
