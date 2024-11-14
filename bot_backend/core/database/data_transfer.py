from csv import reader

from pandas import DataFrame
from sqlalchemy import select

from core.database.models import User
from core.middleware.settings import CSV_PATH
from engine import get_async_session


async def export_users_to_csv():
    """
    Export simplified 'User' entities from the database to CSV file.
    Saved as a CSV file in the 'data_dump' directory.

    :return: None
    """

    async for session in get_async_session():
        result = await session.execute(select(User))
        data = result.scalars().all()
        df = DataFrame([user.simple_dict() for user in data])
        df.to_csv(path_or_buf=CSV_PATH, index=False)


async def import_users_from_csv():
    """
    Import user data from a CSV file and insert it into the 'Users' table
    using SQLAlchemy.

    :return: None
    """

    with open(CSV_PATH, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = reader(file)
        headers = next(csv_reader)

        async for session in get_async_session():
            for row in csv_reader:
                user = User(
                    chat_id=int(row[headers.index('chat_id')]),
                    username=row[headers.index('username')],
                    user_first_name=row[headers.index('user_first_name')],
                    last_tarot_date=None,
                    is_subscribed=row[headers.index('is_subscribed')] == 'True'
                )

                session.add(user)

            await session.commit()
