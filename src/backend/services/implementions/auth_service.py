from services.interfaces.auth_service_interface import Auth_Service_Interface
from repos.implementations.auth_repo import Auth_Repo
import bcrypt


class Auth_Service(Auth_Service_Interface):
    def __init__(self):
        self.auth_repo = Auth_Repo()

    def check_if_user_exists(self, username):
        return self.auth_repo.check_if_user_exists(username)

    def validate_user(self, username, password):
        found_user = self.auth_repo.retrieve_user_by_username(username)
        print(found_user)
        if found_user is None:
            return False
        else:
            db_password = found_user["pw_hash"]
            is_password_correct = bcrypt.checkpw(password.encode(), db_password.encode())
            del found_user["pw_hash"]
            return found_user

    def register_user(self, username, email, password):
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        # Having to decode below is a Postgres specific issue, see:
        # https://stackoverflow.com/a/38262440
        hashed_pw_decoded = hashed_pw.decode("utf8")
        self.auth_repo.register_user(username, email, hashed_pw_decoded)
