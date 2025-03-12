class CustomException(Exception):
    """Excepción personalizada para la aplicación."""

    def __init__(self, message):
        """Inicializa la excepción con un mensaje personalizado."""
        super().__init__(f"❌ Error: {message}")
