from thyme.tracker import launch_tracker
from thyme.frontend import launch_frontend


if __name__ == '__main__':
    print("Launching Tracker")
    tracker_process = launch_tracker()
    print("Launching Frontend")
    frontend_process = launch_frontend()
