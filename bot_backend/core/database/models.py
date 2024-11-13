from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.middleware.settings import TZ


class Base(DeclarativeBase):
    """Base class for declarative models.

    Attributes:
        id (Mapped[int]): Primary key column.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    """
    Represents a user in the database.

    Attributes:
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
        argument='UserMessage',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def simple_dict(self):
        return {
            'chat_id': self.chat_id,
            'username': self.username,
            'user_first_name': self.user_first_name,
            'is_subscribed': self.is_subscribed
        }


class UserMessage(Base):
    """
    Represents a user's message in the database.

    Attributes:
        user_id (int): Foreign key referencing the `Users.id` field, indicating
            which user sent the message.
        message_id (int): Unique identifier for the message within the chat.
        message_date (datetime): Timestamp of when the message was sent.
            Defaults to the current time.

    Relationships:
        user: Many-to-one relationship with the `User` model, indicating the
            user who sent the message.
    """

    __tablename__ = 'Message_ids'

    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    message_id: Mapped[int] = mapped_column()
    message_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(TZ),
        nullable=False,
    )

    user = relationship(argument='User', back_populates='messages')
