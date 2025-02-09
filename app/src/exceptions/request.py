class RequestException(Exception):
    """
    Исключение для ошибок запросов
    """

    def __init__(self, message: str, details: str = ""):
        self.message = message
        self.details = details
        super().__init__(f"{message}: {details}")