import threading
from typing import List

from cough_detector import CoughDetector
from rotation_controller import run_rotation_controller
from settings import settings
from speed_controller import run_speed_controller


def main():
    threads: List[threading.Thread] = []

    cough_detector = CoughDetector(settings.model.path)

    cough_detector_thread: threading.Thread | None = None
    rotate_controller_thread: threading.Thread | None = None
    speed_controller_thread: threading.Thread | None = None

    try:
        rotate_controller_thread = threading.Thread(target=run_rotation_controller)
        cough_detector_thread = threading.Thread(target=cough_detector.run)
        speed_controller_thread = threading.Thread(target=run_speed_controller)

        threads.append(rotate_controller_thread)
        threads.append(cough_detector_thread)
        threads.append(speed_controller_thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, shutting down...")
        cough_detector.stop()
    finally:
        for thread in threads:
            if thread is not None and thread.is_alive():
                thread.join()

        print("Shutdown complete")


if __name__ == "__main__":
    main()
