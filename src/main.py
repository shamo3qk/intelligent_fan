import threading

from cough_detector import CoughDetector
from Finger_counter import exec
from RotateControl import exec1
from settings import settings


def main():
    cough_detector = CoughDetector(settings.model.path)
    cough_detector_thread: threading.Thread | None = None
    finger_counter_thread: threading.Thread | None = None
    rotate_controller_thread: threading.Thread | None = None

    try:
        finger_counter_thread = threading.Thread(target=exec)
        rotate_controller_thread = threading.Thread(target=exec1)
        cough_detector_thread = threading.Thread(target=cough_detector.run)

        finger_counter_thread.start()
        rotate_controller_thread.start()
        cough_detector_thread.start()

        finger_counter_thread.join()
        rotate_controller_thread.join()
        cough_detector_thread.join()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, shutting down...")
        cough_detector.stop()
    finally:
        if finger_counter_thread is not None and finger_counter_thread.is_alive():
            finger_counter_thread.join()
        if rotate_controller_thread is not None and rotate_controller_thread.is_alive():
            rotate_controller_thread.join()
        if cough_detector_thread is not None and cough_detector_thread.is_alive():
            cough_detector_thread.join()

        print("Shutdown complete")


if __name__ == "__main__":
    main()
