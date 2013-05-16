from time import sleep

from thyme.tracker import track
from thyme.database import initialize_database

if __name__ == '__main__':
    session = initialize_database()
    track(session)
