class CustomException(Exception):
    def __init__(self, message):
        super().__init__(f"❌ Error: {message}")
