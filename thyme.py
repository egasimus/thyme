from thyme.tracker import track
from thyme.database import init_db
from thyme.frontend import launch_frontend


if __name__ == '__main__':
    frontend_process = launch_frontend()
    session = init_db()
    track(session)
