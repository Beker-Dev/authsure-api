import argparse

from app.utils.database_utils.populate_database import PopulateDatabase
from app.core.dependencies import get_db

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--populate-db', action='store_true', help='Populate the database')
    parser.add_argument('--reset-db', action='store_true', help='Reset the database')
    arguments = parser.parse_args()

    if arguments.populate_db:
        print(f'{"Starting to populate database":-^50}')
        session = next(get_db())
        db = PopulateDatabase(db_session=session)
        db.populate(arguments.reset_db)
        session.close()
        print(f'{"Finished to populate database":-^50}')
