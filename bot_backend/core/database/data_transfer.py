from csv import reader
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pandas import DataFrame
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.components.settings import DATA_PATH, TZ_STR
from core.database.models import User
from db_connection import async_session_maker


async def export_users_to_csv():
    """
    Export simplified 'User' entities from the database to CSV file.
    Saved as a CSV file in the 'data' directory.

    :return: None
    """

    date = datetime.now(ZoneInfo(TZ_STR)).strftime(
        "date_%d_%m_%Y_time_%H_%M_%S"
    )
    csv_path = DATA_PATH / f'Users_{date}.csv'

    async with async_session_maker() as session:
        result = await session.execute(select(User))
        data = result.scalars().all()
        df = DataFrame([user.simple_dict() for user in data])
        df.to_csv(path_or_buf=csv_path, index=False)


async def import_users_from_csv():
    """
    Import user data from CSV files starting with 'Users' and ending
    with '.csv', insert data into the 'Users' table using SQLAlchemy.
    Logs error if more than one matching file is found.
    """

    csv_files = list(Path(DATA_PATH).glob('Users*.csv'))

    if len(csv_files) > 1:
        print('Ошибка: найдено больше одного файла шаблона "Users*.csv"')
        return

    if len(csv_files) == 0:
        print('Ошибка: не найдено файлов шаблона "Users*.csv"')
        return

    csv_path = csv_files[0]

    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = reader(file)
        headers = next(csv_reader)

        async with async_session_maker() as session:
            for row in csv_reader:
                user = User(
                    chat_id=int(row[headers.index('chat_id')]),
                    username=row[headers.index('username')],
                    user_first_name=row[headers.index('user_first_name')],
                    last_tarot_date=None,
                    is_subscribed=row[headers.index('is_subscribed')] == 'True'
                )

                try:
                    session.add(user)
                    await session.commit()
                except SQLAlchemyError:
                    await session.rollback()
