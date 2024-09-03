from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class inherited from the declarative class."""

    pass


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier.
        chat_id (int): Unique identifier for the user in a chat application.
        username (str): Username of the user, limited to 32 characters.
        user_first_name (str): First name of the user, limited to
            32 characters.
        last_tarot_date (datetime, optional): Timestamp of the last tarot
            reading for the user. This field can be null.
        is_subscribed (bool, optional): Subscription status of the user. This
            field can be null.

    Relationships:
        messages: One-to-many relationship with the `Message` model.
            All associated messages will be deleted if the user is deleted.
    """

    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(32))
    user_first_name: Mapped[str] = mapped_column(String(32))
    last_tarot_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None,
    )
    is_subscribed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        default=None
    )

    messages = relationship(
        'Message',
        back_populates='user',
        cascade='all, delete-orphan'
    )


class Message(Base):
    """
    Represents a user's message in the database.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier for
            each message.
        chat_id (int): Foreign key referencing the `Users.id` field, indicating
            which user sent the message.
        message_id (int): Unique identifier for the message within the chat.
        message_date (datetime): Timestamp of when the message was sent.
            Defaults to the current time.

    Relationships:
        user: Many-to-one relationship with the `User` model, indicating the
            user who sent the message.
    """

    __tablename__ = 'Message_ids'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    message_id: Mapped[int] = mapped_column()
    message_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    user = relationship('User', back_populates='messages')