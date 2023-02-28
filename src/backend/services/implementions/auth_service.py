from services.interfaces.auth_service_interface import Auth_Service_Interface
from repos.implementations.auth_repo import Auth_Repo
import hashlib

class Auth_Service(Auth_Service_Interface):

    def __init__(self):
        self.auth_repo = Auth_Repo()

    def check_if_user_exists(self, username):
        return self.auth_repo.check_if_user_exists(username)
    
    def validate_user(self, username, password):
        hashed_pw = hashlib.md5(password.encode())
        return self.auth_repo.validate_user(username, hashed_pw.hexdigest() )

    def register_user(self, username, email, password):
        hashed_pw = hashlib.md5(password.encode())
        self.auth_repo.register_user(username,email,hashed_pw.hexdigest())