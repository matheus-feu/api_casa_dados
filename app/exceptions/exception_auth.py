class NotAuthenticatedException(Exception):
    def __init__(self):
        super().__init__("Usuário não autenticado")
