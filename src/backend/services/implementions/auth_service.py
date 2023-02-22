from services.interfaces.auth_service_interface import Auth_Service_Interface
from repos.implementations.auth_repo import Auth_Repo
from database import query_db, insert_in_db
import hashlib

class Auth_Service(Auth_Service_Interface):

    def __init__(self):
        self.auth_repo = Auth_Repo()

    def check_if_user_exists(self, username):
        return self.auth_repo.check_if_user_exists(username)
    
    def validate_user(self, username, password):
        return self.auth_repo.validate_user(username,password)

    def register_user(self, username, email, password):
        self.auth_repo.register_user(username,email,password)
