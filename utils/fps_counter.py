# fps_counter.py

import time

class FPSCounter:
    def __init__(self, avg_factor=0.9):
        """
        Initialize the FPS counter.

        Parameters:
        - avg_factor: The weight given to the previous FPS value when calculating the running average.
                     It should be a value between 0 and 1. Closer to 1 means slower adaptation to changes.
        """
        self._start_time = None
        self._frame_count = 0
        self._fps = None
        self._avg_factor = avg_factor

    def start(self):
        """ Start the FPS counter """
        self._start_time = time.time()

    def stop(self):
        """ Stop the FPS counter """
        self._start_time = None
        self._frame_count = 0

    def update(self):
        """ Call this method once for every frame processed """
        self._frame_count += 1
        elapsed_time = time.time() - self._start_time
        current_fps = self._frame_count / elapsed_time

        # Compute the running average FPS
        if self._fps is None:
            self._fps = current_fps
        else:
            self._fps = (self._avg_factor * self._fps) + (1.0 - self._avg_factor) * current_fps

    def get_fps(self):
        """ Get the current FPS estimate """
        return self._fps
