import logging
from signal import SIGINT, SIGTERM, signal

logger = logging.getLogger(__name__)


class SignalHandler:
    def __init__(self):
        self.received_signal = False
        signal(SIGINT, self._signal_handler)
        signal(SIGTERM, self._signal_handler)

    def _signal_handler(self, signal_type, frame):
        logger.info(f"handling signal {signal_type} {frame}, exiting gracefully")
        self.received_signal = True
