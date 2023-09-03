import bcrypt


class Password:
    @classmethod
    def encrypt(cls, pw: str):
        return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def check(cls, pw: str, db_pw: str):
        return bcrypt.checkpw(pw.encode(), db_pw.encode())
