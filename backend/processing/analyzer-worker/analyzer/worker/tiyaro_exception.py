class TiyaroException(RuntimeError):
    def __init__(self, error_message: str):
        self.error_message = error_message
