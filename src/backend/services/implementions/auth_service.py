from services.interfaces.auth_service_interface import Auth_Service_Interface
from repos.orm.implementations.auth_queries import Auth_Repo
from util.custom_exceptions import Custom_Exception
import bcrypt


class Auth_Service(Auth_Service_Interface):
    def __init__(self):
        self.auth_repo = Auth_Repo()

    def check_if_user_exists(self, username):
        found_user = self.auth_repo.check_if_user_exists(username)
        if found_user is None:
            raise Custom_Exception(status_code=404,msg="User not found")
        return found_user

    def validate_user(self, username, password):
        found_user = self.auth_repo.validate_user(username)
        if found_user is None:
            raise Custom_Exception(status_code=403,msg="username not found")
        else:
            db_password = found_user.pw_hash
            del found_user.pw_hash

            # legacy users have md5 encrypted passwords that need to be encrypted with bcrypt instead 
            if not db_password.startswith("$2b$"):
                # the user is a legacy user and only then will we import the hashlib library (to avoid bloat)
                import hashlib
                
                if hashlib.md5(password.encode()).hexdigest() != db_password:
                    # handling the edge case that a user has found a legacy account but provides incorrect password
                    raise Custom_Exception(status_code=403,msg="username not found")
                else: 
                    self.reset_password(password, found_user.user_id)
                    return found_user
                
            if bcrypt.checkpw(password.encode(), db_password.encode()):
                return found_user
            else:
                raise Custom_Exception(status_code=403,msg="Password is Incorrect")

    def register_user(self, username, email, password):
        if self.auth_repo.check_if_user_exists(username):
            raise Custom_Exception(status_code=403,msg="User already exists")

        if self.auth_repo.check_if_email_is_taken(email):
            raise Custom_Exception(status_code=403,msg="Email is already taken")

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        # Having to decode it is a Postgres specific issue, see:
        # https://stackoverflow.com/a/38262440
        hashed_pw_decoded = hashed_pw.decode("utf8")
        self.auth_repo.register_user(username, email, hashed_pw_decoded)

    def reset_password(self, password, user_id):
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        hashed_pw_decoded = hashed_pw.decode("utf8")
        self.auth_repo.change_user_password(hashed_pw_decoded, user_id)
