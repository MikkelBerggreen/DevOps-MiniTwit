from services.interfaces.auth_service_interface import Auth_Service_Interface
from repos.orm.implementations.auth_queries import Auth_Repo
import bcrypt


class Auth_Service(Auth_Service_Interface):
    def __init__(self):
        self.auth_repo = Auth_Repo()

    def check_if_user_exists(self, username):
        return self.auth_repo.check_if_user_exists(username)

    def validate_user(self, username, password):
        found_user = self.auth_repo.validate_user(username)
        if found_user is None:
            return None
        else:
            db_password = found_user["pw_hash"]
            del found_user["pw_hash"]

            # legacy users have md5 encrypted passwords that need to be encrypted with bcrypt instead 
            if not db_password.startswith("$2b$"):
                # the user is a legacy user and only then will we import the hashlib library (to avoid bloat)
                import hashlib
                
                if hashlib.md5(password.encode()).hexdigest() != db_password:
                    # handling the edge case that a user has found a legacy account but provides incorrect password
                    return None
                else: 
                    self.reset_password(password, found_user["user_id"])
                    return found_user
                
            is_password_correct = bcrypt.checkpw(password.encode(), db_password.encode())
            return found_user

    def register_user(self, username, email, password):
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        # Having to decode it is a Postgres specific issue, see:
        # https://stackoverflow.com/a/38262440
        hashed_pw_decoded = hashed_pw.decode("utf8")
        self.auth_repo.register_user(username, email, hashed_pw_decoded)

    def reset_password(self, password, user_id):
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        hashed_pw_decoded = hashed_pw.decode("utf8")
        self.auth_repo.change_user_password(hashed_pw_decoded, user_id)
