from passlib.context import CryptContext  # install bcrypt schemes


class Hash():
    def bcrypt(password: str):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)
