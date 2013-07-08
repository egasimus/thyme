from thyme.tracker import launch_tracker
from thyme.frontend import launch_frontend


if __name__ == '__main__':
    tracker_process = launch_tracker()
    launch_frontend()
